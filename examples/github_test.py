from github import Github

# First create a Github instance:
g = Github('13cdc94e05bbde67b622cf343bf0366a6415fb60')

# Then play with your Github objects:
# for repo in g.get_user().get_repos():
#     print repo.name

for repo in g.get_user().get_gists():
    print gist.name