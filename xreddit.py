
import cmd
import sys

import natural_cmd
import hacker_cmd

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "hacker":
            hacker_cmd.HackerCmd.prompt = 'xreddit > '
            hacker_cmd.HackerCmd().cmdloop()
    else:
        natural_cmd.RedditCmd.prompt = 'xreddit > '
        natural_cmd.RedditCmd().cmdloop()


