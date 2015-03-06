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

        p = Popen('git log --format="%s" -n 10' % GIT_LOG_FORMAT, shell=True,
                  stdout=PIPE)

        (log, _) = p.communicate()
        log = log.strip('\n\x1e').split("\x1e")

        log = [row.strip().split("\x1f") for row in log]
        log = [dict(zip(GIT_COMMIT_FIELDS, row)) for row in log]

        return log

    def gitdiff(self, commitId):
        return check_output(['git', 'diff', '%s^..%s' % (commitId, commitId)])

    def printcherrypicks(self):
        logs = self.parselastcommit()
        for log in logs:
            portedCommit = log['id']
            m = re.search('cherry picked from commit ([a-z0-9A-Z]+)', log[
                'body'] + log['subject'])
            if m is not None:
                m = re.search('This reverts commit ([a-z0-9A-Z]+)', log[
                    'body'] + log['subject'])
            if (m):
                originalId = m.group(1)
                print (originalId + ' being compared to current commit ' + portedCommit)

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
                print ('No revert or cherry pick commit found in ' + portedCommit)
Glog().printcherrypicks()
