The output of git log --all -- preprocess.db (to check if the file still exists in any commit)

        commit 1951c43f6d67961e8aa72801855a74342f3e3d02
        Author: Jane <Kim>
        Date:   Sat Jun 22 16:20:44 2024 -0700

            Remove LFS tracking and update .gitignore

        commit e582feb67ab3a60febdcfb2df04889f1e9cfebe3
        Author: Jane <Kim>
        Date:   Thu Jun 20 19:15:40 2024 -0700

            Separating tipitaka_db into three by baskets; Debugging ingest functions

        commit 45ac027a53a9b955748873d29667075c479066a1
        Author: Jane <Kim>
        Date:   Thu Jun 20 18:15:11 2024 -0700

            fixed load_demormalized_children_to_db: issue with json string not being recognized; finished cleanup script fo
        r sutta load tables

        commit 386620de4f469b41a1f777e4200212dbfeba495f
        Author: Jane <Kim>
        Date:   Thu Jun 20 15:04:30 2024 -0700

            refactor: Cleanup and optimize preprocessing scripts

        commit 6bdfd156007b1d4057e99620b8b906025254bfd0
        Author: Jane <Kim>
        Date:   Wed Jun 19 21:46:35 2024 -0700

            add preprocess.db with lfs

        commit dada04ae36368693db436de65f817bc0a7507590
        Author: Jane <Kim>
        Date:   Wed Jun 19 21:36:17 2024 -0700

            writing cleanup scripts for load tables

The contents of your .gitignore file

        notes.md
        sc-data/
        sutta.db
        vinaya.db
        abhidhamma.db
        preprocess.db

The output of git status (to see if there are any uncommitted changes)

        On branch dev
        Your branch is ahead of 'origin/dev' by 13 commits.
        (use "git push" to publish your local commits)

        Changes not staged for commit:
        (use "git add/rm <file>..." to update what will be committed)
        (use "git restore <file>..." to discard changes in working directory)
                deleted:    .gitattributes
                modified:   README.md
                deleted:    preprocess.db

        Untracked files:
        (use "git add <file>..." to include in what will be committed)
                git.sh

        no changes added to commit (use "git add" and/or "git commit -a")