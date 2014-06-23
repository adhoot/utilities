import math
import os
import re
from subprocess import PIPE, Popen, check_call, check_output

__author__ = 'adhoot'

class Glog:

    def parselastcommit(self):
        GIT_COMMIT_FIELDS = ['id', 'author_name', 'author_email', 'date',
                             'subject', 'body']
        GIT_LOG_FORMAT = ['%H', '%an', '%ae', '%ad', '%s', '%b']
        GIT_LOG_FORMAT = '%x1f'.join(GIT_LOG_FORMAT) + '%x1e'

        #os.chdir('/Users/adhoot/code/apache-hadoop')
        p = Popen('git log --format="%s" -n 10' % GIT_LOG_FORMAT, shell=True,
                  stdout=PIPE)

        (log, _) = p.communicate()
        log = log.strip('\n\x1e').split("\x1e")
        log = [row.strip().split("\x1f") for row in log]
        log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]
        # print(log)
        return log

    def gitdiff(self, commitId):
        return check_output(['git', 'diff', '%s^..%s' % (commitId, commitId)])

    def printcherrypicks(self):
        logs = self.parselastcommit()
        for log in logs:
            # print ('body=>' + log['body'])
            portedCommit = log['id']
            originalId = ''
            m = re.search('cherry picked from commit ([a-z0-9A-Z]+)', log[
                'body'])
            if m:
                originalId = m.group(1)
                print (originalId + ' was ported into ' + portedCommit)

                conflictorig_patch = '/tmp/conflictorig.patch'
                originalDiffPatch = open(conflictorig_patch, 'w')
                originalDiffPatch.write(self.gitdiff(originalId))
                originalDiffPatch.close()

                conflictported_patch = '/tmp/conflictported.patch'
                portedDiffPatch = open(conflictported_patch, 'w')
                portedDiffPatch.write(self.gitdiff(portedCommit))
                portedDiffPatch.close()

                check_call(["diffmerge", conflictorig_patch, conflictported_patch])
            else:
                print ('No cherry pick commit found')

    def demo(self):
        a = int(input("a "))
        b = int(input("b "))
        c = int(input("c "))
        d = b ** 2 - 4 * a * c
        disc = math.sqrt(d)
        root1 = (-b + disc) / (2 * a)
        root2 = (-b - disc) / (2 * a)
        print(root1, root2)
Glog().printcherrypicks()
