# Create a new branch without any history
git checkout --orphan temp_branch

# Add all files to the new branch
git add -A

# Commit the changes
git commit -am "Initial commit"

# Delete the old branch
git branch -D dev

# Rename the temporary branch to your main branch
git branch -m dev

# Force push the new branch
git push -f origin dev