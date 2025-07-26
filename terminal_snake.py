
import random
import time
import curses
def main(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

    snk_x = sw // 4
    snk_y = sh // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]
    food = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
    w.addch(food[0], food[1], '*')

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = w.getch()
        key = key if next_key == -1 else next_key

        # Calculate new head
        head = [snake[0][0], snake[0][1]]
        if key == curses.KEY_DOWN:
            head[0] += 1
        if key == curses.KEY_UP:
            head[0] -= 1
        if key == curses.KEY_LEFT:
            head[1] -= 1
        if key == curses.KEY_RIGHT:
            head[1] += 1

        # Check for collision
        if (
            head[0] in [0, sh] or
            head[1] in [0, sw] or
            head in snake
        ):
            msg = f'Game Over! Score: {score}  Press any key to exit.'
            w.addstr(sh // 2, sw // 2 - len(msg) // 2, msg)
            w.nodelay(0)
            w.getch()
            break

        snake.insert(0, head)
        if head == food:
            score += 1
            food = None
            while food is None:
                nf = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
                if nf not in snake:
                    food = nf
            w.addch(food[0], food[1], '*')
        else:
            tail = snake.pop()
            w.addch(tail[0], tail[1], ' ')

        w.addch(snake[0][0], snake[0][1], '#')
        w.addstr(0, 2, f'Score: {score} ')

if __name__ == '__main__':
    curses.wrapper(main) 