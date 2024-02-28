"""Client code to test the code."""

from pysvc.objects import Commit, File, Tree

if __name__ == '__main__':
    file1 = File(contents='first file')
    file2 = File(contents='second file')
    file3 = File(contents='third file')

    tree1 = Tree(objects={'file1.txt': file1, 'file2.txt': file2})
    tree2 = Tree(objects={'file3.txt': file3, 'subfolder': tree1})

    commit = Commit(
        tree_hash=tree2.get_object_hash(), message='Initial commit'
    )

    print(commit.get_object_contents())

    a: int = 10
    a = 20
