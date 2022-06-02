let board = Array(9).fill("");
let game_over = false;
let winning_blocks = Array(3).fill(-1);

const board_container = document.querySelector(".board");
const outcome_container = document.querySelector(".outcome");
const restart_container = document.querySelector(".restart");

const player = "X";
const nao = "O";
const draw = "D";

const render_board = () => {
    html = "";
    board.forEach((e, i) => {
        if (i % 3 === 0) {
            html += `<div class="row">`;
        }

        if (e == player || e == nao || game_over) {
            if (winning_blocks.includes(i)) {
                html += `<div id="block_${i}" class="col-4 block winning"><h1 class="text-center">${e}</h1></div>`
            } else {
                html += `<div id="block_${i}" class="col-4 block occupied"><h1 class="text-center">${e}</h1></div>`
            }
        } else {
            html += `<div id="block_${i}" class="col-4 block" onclick="player_move(${i})"><h1 class="text-center">${e}</h1></div>`
        }
        
        if (i % 3 === 2) {
            html += `</div>`;
        }
    });

    board_container.innerHTML = html;
}

render_board();

const player_move = (i) => {
    if (board[i] == "") {
        board[i] = player;
    }

    game_loop();

    if (!game_over) {
        nao_move();
    }
}

const nao_move = () => {
    do {
        i = Math.floor(Math.random() * 9);
    } while (board[i] != "");
    board[i] = nao;
    game_loop();
}

const game_loop = () => {    
    outcome = check_winner();
    if (outcome == player) {
        outcome_container.innerHTML = `<h2>Player wins!</h2>`;
        game_over = true;
    } else if (outcome == nao) {
        outcome_container.innerHTML = `<h2>NAO wins!</h2>`;
        game_over = true;
    } else if (check_board_complete()) {
        outcome_container.innerHTML = `<h2>Draw</h2>`;
        game_over = true;
    }

    render_board();
    
    if (game_over) {
        restart_container.innerHTML = `<button type="button" class="btn btn-primary" onclick="restart()">Play Again</button>`;
    }
};

const check_board_complete = () => {
    for (i = 0; i < 9; i++) {
        if (board[i] == "") {
            return false;
        }
    }
    return true;
}

const check_winner = () => {
    for (i = 0; i < 9; i += 3) {
        if (check_line(i, i + 1, i + 2)) {
            winning_blocks = [i, i + 1, i + 2]
            return board[i];
        }
    }

    for (i = 0; i < 3; i++) {
        if (check_line(i, i + 3, i + 6)) {
            winning_blocks = [i, i + 3, i + 6];
            return board[i];
        }
    }

    if (check_line(0, 4, 8)) {
        winning_blocks = [0, 4, 8];
        return board[0];
    }

    if (check_line(2, 4, 6)) {
        winning_blocks = [2, 4, 6];
        return board[2];
    }
}

const check_line = (a, b, c) => {
    return (
        board[a] == board[b] &&
        board[b] == board[c] &&
        (board[a] == player || board[a] == nao)
    );
}

const restart = () => {
    outcome_container.innerHTML = "";
    restart_container.innerHTML = "";

    board = Array(9).fill("");
    game_over = false;
    winning_blocks = Array(3).fill(-1);

    game_loop();
}
