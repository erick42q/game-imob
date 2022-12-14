from .player import Player
from .ground import Ground
from dataclasses import dataclass
from random import randint, getrandbits
from .tools import vprint


@dataclass
class Match:

    players: list[Player]
    winner: Player = None
    _timeout = False
    rounds = int

    def roll_dice(self):
        steps = randint(1, 6)
        return steps

    def transaction(self, player: dataclass, propriedade: dataclass):
        if propriedade.owner and propriedade.owner != player:
            player.pagar(propriedade.rent_value)
            return

        if player.balance >= propriedade.sale_value:
            if player.tipo == 'inpulsivo':
                player.buy_prop(propriedade)

            elif player.tipo == 'exigente' and propriedade.rent_value > 50:
                player.buy_prop(propriedade)

            elif player.tipo == 'cauteloso' and (player.balance - propriedade.sale_value) >= 80:
                player.buy_prop(propriedade)

            elif player.tipo == 'aleatório':
                if bool(getrandbits(1)):
                    player.buy_prop(propriedade)

                else:
                    vprint(f'           ###{player.tipo} não quis comprar a propriedade')

    def game_over(self, player: dataclass):
        if player.balance <= 0:
            self.players.remove(player)
            vprint(f'O jogador {player.tipo} não tem mais recursos e está fora da partida\n')

    def has_winner(self):
        if len(self.players) == 1:
            self.winner = self.players[0]
            return True
        return False

    def show_players(self):
        msg = ''
        vprint('Começando o game:\n')
        for player in self.players:
            msg += f'    jogador: {player.tipo}\n    saldo: {player.balance}\n\n'
        return msg

    def victory_announce(self, winner: Player, grounds: list[Ground]):
        vprint('================================================================')
        vprint('TEMOS UM VENCEDOR \o/')
        vprint(f'{winner.tipo}:')
        vprint(
            f"""
            saldo: {winner.balance}
            total de propriedades: {winner.prop_owned(grounds)}
            """
        )
        vprint('================================================================\n')

    def timeout(self):
        self._timeout = True
        for player in self.players:
            if not self.winner:
                self.winner = player
            if self.winner.balance < player.balance:
                self.winner = player
