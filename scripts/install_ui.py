"""Four-step keyboard installer; caller supplies ownership and destinations."""
import curses
import os
import shutil
import sys


def supported():
    size = shutil.get_terminal_size(fallback=(0, 0))
    term = os.environ.get('TERM', 'dumb')
    return sys.stdin.isatty() and sys.stdout.isatty() and size.lines >= 23 and size.columns >= 50 and term.startswith(('xterm', 'screen', 'tmux', 'rxvt', 'ansi', 'linux', 'alacritty', 'wezterm', 'kitty', 'iterm'))


def choose(agents, roots, selected_agents, selected_roots, copy, target_for, owned, retired_for=lambda target, roots: []):
    """Return (agents, roots, copy), or None on cancellation."""
    selected_agents = set(selected_agents)
    selected_roots = set(selected_roots)

    def run(screen):
        nonlocal copy
        screen.keypad(True)
        try:
            curses.curs_set(0)
        except curses.error:
            pass
        step = 0
        positions = [0, 0, int(copy), 0]
        error = ''
        while True:
            screen.erase()
            height, width = screen.getmaxyx()
            def line(row, text, highlight=False):
                if row < height - 1:
                    try:
                        screen.addnstr(row, 2, text, max(0, width - 4), curses.A_REVERSE if highlight else curses.A_NORMAL)
                    except curses.error:
                        pass
            line(1, 'FUDGE / Install skills')
            line(2, f'Step {step + 1} of 4')
            titles = ['Choose target agents', 'Choose public skills', 'Choose install method', 'Review installation']
            line(4, titles[step])
            if step < 3:
                choices = agents if step == 0 else roots if step == 1 else ['Symlink', 'Copy']
                for index, choice in enumerate(choices):
                    selected = choice in selected_agents if step == 0 else choice in selected_roots if step == 1 else index == int(copy)
                    line(6 + index, f'[{"x" if selected else " "}] {choice}', positions[step] == index)
            else:
                rows = [f'Method: {"Copy" if copy else "Symlink"}']
                conflicts = []
                for agent in agents:
                    if agent not in selected_agents:
                        continue
                    rows.append(f'Target: {agent} ({target_for(agent)})')
                    for root in roots:
                        if root not in selected_roots:
                            continue
                        path = target_for(agent) / ('fudge-' + root)
                        exists = path.exists() or path.is_symlink()
                        state = 'conflict' if exists and not owned(path) else 'update' if exists else 'new'
                        rows.append(f'  {state}: fudge:{root}')
                        if state == 'conflict':
                            conflicts.append(str(path))
                cleanup = [path for agent in agents if agent in selected_agents
                           for path in retired_for(target_for(agent), selected_roots)]
                if cleanup:
                    rows += ['Retired entries to remove:'] + [str(path) for path in cleanup]
                if conflicts:
                    rows += ['Resolve or deselect foreign conflicts before installing.'] + conflicts
                visible = max(1, height - 12)
                positions[3] = min(positions[3], max(0, len(rows) - visible))
                for row, text in enumerate(rows[positions[3]:positions[3] + visible], 6):
                    line(row, text)
            line(height - 5, error)
            line(height - 3, 'Up/Down move  Space select  Enter continue' if step < 3 else 'Up/Down browse  Enter install')
            line(height - 2, 'Esc back/cancel  q cancel')
            screen.refresh()
            key = screen.getch()
            error = ''
            if key in (ord('q'), ord('Q'), 4):
                return None
            if key == 27:
                if step == 0:
                    return None
                step -= 1
            elif key in (curses.KEY_UP, curses.KEY_DOWN):
                direction = -1 if key == curses.KEY_UP else 1
                if step == 3:
                    positions[3] = max(0, min(max(0, len(rows) - visible), positions[3] + direction))
                else:
                    positions[step] = (positions[step] + direction) % len(choices)
            elif key == ord(' ') and step < 3:
                if step == 2:
                    copy = bool(positions[2])
                else:
                    selected = selected_agents if step == 0 else selected_roots
                    choice = choices[positions[step]]
                    selected.remove(choice) if choice in selected else selected.add(choice)
            elif key in (10, 13, curses.KEY_ENTER):
                if step == 0 and not selected_agents:
                    error = 'Select at least one agent.'
                elif step == 1 and not selected_roots:
                    error = 'Select at least one public skill.'
                elif step == 3:
                    if conflicts:
                        error = 'Resolve or deselect conflicts before installing.'
                    else:
                        return ([a for a in agents if a in selected_agents], [r for r in roots if r in selected_roots], copy)
                else:
                    step += 1
    return curses.wrapper(run)
