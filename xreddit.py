
import cmd
import sys

import natural_cmd
import hacker_cmd

# NEED TO BE DONE

# some pages have an extra post with no rank and others don't, sort accordingly
# check {attr['class': 'domain']} for the redirect site (reddit, facebook, youtube, etc)
# include number of upvotes
# also need to probably  include a way to upvote as user, api call?
# message system @user
# different tabs in each subreddit (hot, new, rising, controversial, etc.)
# clean up

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "hacker":
            hacker_cmd.HackerCmd.prompt = 'xreddit > '
            hacker_cmd.HackerCmd().cmdloop()
    else:
        natural_cmd.HelloWorld.prompt = 'xreddit > '
        natural_cmd.HelloWorld().cmdloop()


