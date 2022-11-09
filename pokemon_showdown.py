import json
import os
import pexpect
import time


class PSBattle:

    def __init__(self, format_id="gen1ou", log=False, teams=[None, None], debug=False):

        self.log = log
        self.format_id = format_id
        self.root_uuid = None
        self.teams = teams
        self.debug = debug

        self.startup(self.format_id)
        self.freeze()

    def startup(self, format_id):
        """Launch random battle."""
        self.analyzer = pexpect.spawn("{}/pokemon-showdown".format(os.environ["PS_ROOT"]),
                                      ["simulate-battle"], encoding='utf-8')
        if self.debug:
            self.analyzer.expect('\r\n\r\n')
        self.analyzer.sendline('>start {{"formatid":"{}"}}'.format(format_id))
        self.analyzer.expect('\r\n\r\n')
        if self.teams[0]:
            self.analyzer.sendline('>player p1 {{"name":"Player 1", "team":{}}}'.format(self.teams[0]))
        else:
            self.analyzer.sendline('>player p1 {"name":"Player 1"}')
        self.analyzer.expect('\r\n\r\n')
        if self.teams[1]:
            self.analyzer.sendline('>player p2 {{"name":"Player 2", "team":{}}}'.format(self.teams[1]))
        else:
            self.analyzer.sendline('>player p2 {"name":"Player 2"}')
        self.analyzer.expect('\r\n\r\n')
        self.analyzer.expect('\r\n\r\n')
        self.analyzer.expect('\r\n\r\n')

    def freeze(self):
        """Freeze the battle status."""
        self.analyzer.sendline('>freeze')
        self.analyzer.expect('uuid: ')
        if self.log:
            print(self.analyzer.before)
            if 'error' in self.analyzer.before:
                raise Exception('Error occurred while sending instructions to the battle')
        self.analyzer.expect('\r\n\r\n')
        self.uuid = self.analyzer.before
        # self.state = json.loads(open("{}.txt".format(self.uuid), "r").read())
        self.state = PSBattle.read_state(self.uuid, self.root_uuid)

    def unfreeze(self, uuid):  # saving states internally in the simulator could not be useful anymore
        """Unfreeze the battle status."""
        while not os.path.exists('{}.txt'.format(uuid)):
            time.sleep(.5)
        self.uuid = uuid
        self.startup(self.format_id)
        self.analyzer.sendline('>unfreeze {}'.format(uuid))
        self.analyzer.expect('\r\n\r\n')
        # self.analyzer.expect('uuid: ')
        if self.log:
            print(self.analyzer.before)
            if 'no such file or directory' in self.analyzer.before:
                raise Exception('Error occurred while unfreezing')
        # self.uuid = self.analyzer.before
        # self.state = json.loads(open("{}.txt".format(self.uuid), "r").read())
        self.state = PSBattle.read_state(self.uuid, self.root_uuid)

    @staticmethod
    def read_state(uuid, root_uuid):
        start = time.time()
        while True:
            try:
                state = json.loads(open("{}.txt".format(uuid), "r").read())
                if uuid != root_uuid:
                    os.remove("{}.txt".format(uuid))
                return state
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                pass
            if time.time() - start > 10:
                raise Exception('Failed to read state from disk')

    def need_replacement(self):
        to_be_replaced = []
        for t in range(2):
            team = self.state['sides'][t]['pokemon']
            active = [it for it, pokemon in enumerate(team) if pokemon['isActive']]
            if len(active) == 0:
                to_be_replaced.append(t)
        return to_be_replaced

    def get_available(self, p):
        team = self.state['sides'][p]['pokemon']
        alive = [it+1 for it, pokemon in enumerate(team) if pokemon['hp'] > 0]
        return alive

    def step(self, actions):
        for i in range(2):
            if actions[i] != -1:
                if actions[i][0] == 'm':
                    self.analyzer.sendline('>p{} move {}'.format(i+1, int(actions[i][1])+1))
                else:
                    self.analyzer.sendline('>p{} switch {}'.format(i + 1, int(actions[i][1]) + 1))
        self.freeze()
