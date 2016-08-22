import codecs
from os import path
from operator import itemgetter

from sphinx.builders import Builder
from sphinx.util.osutil import os_path, ensuredir

def setup(app):
    app.add_builder(DocgraphBuilder)

class DocgraphBuilder(Builder):
    name = 'docgraph'

    def get_outdated_docs(self):
        yield self.app.config.master_doc

    def get_target_uri(self, docname, typ=None):
        return ''

    def prepare_writing(self, docnames):
        pass

    def write_doc(self, docname, doctree):
        outfilename = path.join(self.outdir, 'docgraph.txt')
        ensuredir(path.dirname(outfilename))

        try:
            f = codecs.open(outfilename, 'w', 'utf-8')
            try:
                f.write(process_doctree(self.app, doctree, docname))
            finally:
                f.close()
        except (IOError, OSError) as err:
            self.warn("error writing file %s: %s" % (outfilename, err))

def process_doctree(app, doctree, docname):
    traversed = set()

    def traverse_toctree(parent, docname):
        if parent == docname:
            app.env.warn(docname, 'self referenced toctree found. Ignored.')
            return

        # traverse toctree by pre-order
        yield parent, docname
        traversed.add(docname)

        for child in (app.env.toctree_includes.get(docname) or []):
            for subparent, subdocname in traverse_toctree(docname, child):
                if subdocname not in traversed:
                    yield subparent, subdocname
                    traversed.add(subdocname)

    relations = {}
    docnames = traverse_toctree(None, app.config.master_doc)
    prevdoc = None
    for parent, docname in docnames:
        if not parent in relations:
            relations[parent] = []

        relations[parent].append(docname)

    def build_tree(name, children):
        cs = []
        for child in children:
            cs.append(build_tree(child, relations.get(child, [])))

        return (name, cs)

    tree = build_tree('index', relations['index'])

    return stringify_tree(tree)


def stringify_tree(tree, indent='+ '):
    s = indent + tree[0] + "\n"

    for branch in tree[1]:
        s += stringify_tree(branch, '| ' + indent)

    return s
