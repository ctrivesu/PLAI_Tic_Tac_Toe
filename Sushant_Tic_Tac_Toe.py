# SUSHANT TRIVEDI, PLAI - 2 15th June 2019
import sys

class State:
    def children(self):
        '''Returns an iterator over child states.
        NOTE: Valid only if NOT is_terminal().
        '''
        raise NotImplementedError()

    def payoff(self):
        '''Returns the payoff of the state.
        NOTE: Valid only if is_terminal().
        '''
        raise NotImplementedError()

    def payoff_lower(self):
        '''Returns a lower bound on the payoff.'''
        raise NotImplementedError()

    def payoff_upper(self):
        '''Returns an upper bound on the payoff.'''
        raise NotImplementedError()

    def is_terminal(self):
        '''Checks if the state is terminal.'''
        raise NotImplementedError()

    def is_max_player(self):
        '''Checks if the current state is a max player's turn.'''
        raise NotImplementedError()


class TicTacToe(State):
    def __init__(self, board, player, is_max_player, move=None):
        self.board = board
        self.player = player
        self._is_max_player = is_max_player
        self._move = move
        if self.is_max_player():
            self.value = -1
        else:
            self.value = 1


    def children(self):
        player = 'X' if self.player == 'O' else 'O'
        is_max_player = not self._is_max_player

        t = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '_':
                    board = [[x for x in row] for row in self.board]
                    board[r][c] = self.player
                    t.append(TicTacToe(board, player, is_max_player, (r, c)))
        return t

    def payoff(self):
        winner = self._winner()
        if winner is None:
            return 0
        # Either previous min-player won (-1) or previous max-player won (+1).
        return -1 if self._is_max_player else 1

    def is_terminal(self):
        if self._winner() is not None:
            return True

        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '_':
                    return False
        return True

    def is_max_player(self):
        return self._is_max_player

    def move(self):
        '''Returns the move used to transition to this state.'''
        return self._move

    def _winner(self):
        '''Returns the current winner, if one exists.'''
        board = self.board

        for i in range(3):
            # Check rows...
            if board[i][0] != '_' and \
               board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]

            # Check columns...
            if board[0][i] != '_' and \
               board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]

        # Check diagonals...
        if board[0][0] != '_' and \
           board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]

        if board[2][0] != '_' and \
           board[2][0] == board[1][1] == board[0][2]:
            return board[2][0]

        return None


def alpha_beta_minimax(state, alpha, beta):

    if state.is_terminal():
        # print("Terminal State Reached", state._move, "for player ", state.player)
        state.value = state.payoff()
        return state

    else:
        # print("Starting loop for state ", state._move, " for player : ", state.player)
        chil = state.children()
        # if state._move == None:
        #     print(len(chil))
        #     for i in chil:
        #         print(i._move)
        temp = -1
        if state.is_max_player():               # MAX PLAYER
            for next_state in chil:
                state.value = max(state.value, alpha_beta_minimax(next_state, alpha, beta).value)
                alpha = max(state.value, alpha)
                # if state.value >= temp and state._move == None:
                #     temp = state.value
                #     temp_move = next_state._move
                #     print("TEMP MOVE: ", temp_move)
                if alpha >= beta and state._move != None:
                    break
                # if state._move == None:
                #     print("AB UPDMAX: ", state.board, state.value, state.is_max_player(), state.player, next_state.move())
            # if state._move == None:
            #     print("ENTERED")
            #     state._move = temp_move
            return state
        else:
            for next_state in chil:
                state.value = min(state.value, alpha_beta_minimax(next_state, alpha, beta).value)
                beta = min(beta, state.value)
                if alpha >= beta:
                    break
            # print("AB UPDMIN: ", state.board, state.value, state.is_max_player(), state.player, state.move())
            return state



def alpha_beta_minimax_choice(state):
    lower, upper = -1, 1
    value, choice = lower, None

    for s in state.children():
        value_ = alpha_beta_minimax(s, lower, upper)
        if value_.value >= value:
            value, choice = value_.value, s.move()
    return choice

def main():
    player = str(input())
    board = [list(input()) for _ in range(3)]
    state = TicTacToe(board, player, True)
    print("STATE COMPLETED")
    fin_state = alpha_beta_minimax_choice(state)
    print("FIN: ", fin_state)


if __name__ == '__main__':
    main()
