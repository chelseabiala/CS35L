import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      squares: Array(9).fill(null),
      xIsNext: true,
      currentSquare: null,
      numTurns: 0,
    };
  }

  validMove(i) {
    if(this.state.squares[i]) {
      return false;
    }
    let adjacentSquares;
    switch (this.state.currentSquare + 1) {
      case 1:
        adjacentSquares = [2, 4, 5];
        break;
      case 2:
        adjacentSquares = [1, 3, 4, 5, 6];
        break;
      case 3:
        adjacentSquares = [2, 5, 6];
        break;
      case 4:
        adjacentSquares = [1, 2, 5, 7, 8];
        break;
      case 5:
        adjacentSquares = [1, 2, 3, 4, 6, 7, 8, 9];
        break;
      case 6:
        adjacentSquares = [2, 3, 5, 8, 9];
        break;
      case 7:
        adjacentSquares = [4, 5, 8];
        break;
      case 8:
        adjacentSquares = [4, 5, 6, 7, 9];
        break;
      case 9:
        adjacentSquares = [5, 6, 8];
        break;
      default:
        return;
    }
    if (adjacentSquares.includes(i + 1)) {
      return true;
    } else {
      return false;
    }
  }

  canWin(i) {
    let currentTurn = this.state.squares[i];
    switch (i + 1) {
      case 1:
        if (this.state.squares[7] == currentTurn || this.state.squares[5] == currentTurn) {
          return true;
        }
        break;
      case 2:
        if (this.state.squares[8] == currentTurn || this.state.squares[6] == currentTurn) {
          return true;
        }
        break;
      case 3:
        if (this.state.squares[3] == currentTurn || this.state.squares[7] == currentTurn) {
          return true;
        }
        break;
      case 4:
        if (this.state.squares[8] == currentTurn || this.state.squares[2] == currentTurn) {
          return true;
        }
        break;
      case 6:
        if (this.state.squares[0] == currentTurn || this.state.squares[6] == currentTurn) {
          return true;
        }
        break;
      case 7:
        if (this.state.squares[5] == currentTurn || this.state.squares[1] == currentTurn) {
          return true;
        }
        break;
      case 8:
        if (this.state.squares[0] == currentTurn || this.state.squares[2] == currentTurn) {
          return true;
        }
        break;
      case 9:
        if (this.state.squares[1] == currentTurn || this.state.squares[3] == currentTurn) {
          return true;
        }
        break;
    }
    return false;
  }

  handleClick(i) {
    const squares = this.state.squares.slice();
    if (calculateWinner(squares)) {
      return;
    }
    
    if (squares[i]) { 
      if (this.state.numTurns >= 6) { 
        let currentTurn = this.state.xIsNext ? "X" : "O";
        if (currentTurn == squares[i]) {
          if (currentTurn == squares[4] && !this.canWin(i) && i != 4) {
            return;
          }
          this.setState({
            squares: squares,
            currentSquare: i,
          });
        }
      return;
      }
    }  
    
    if (this.state.numTurns >= 6 && this.state.currentSquare != null && this.validMove(i)) {
      squares[i] = this.state.xIsNext ? 'X' : 'O';
      squares[this.state.currentSquare] = null;
      this.setState({
        squares: squares,
        xIsNext: !this.state.xIsNext,
        currentSquare: null,
        numTurns: this.state.numTurns + 1,
      });
      return;
    }
    else if (this.state.numTurns >=6) {
      return;
    }

    if (this.state.numTurns < 6) {

      squares[i] = this.state.xIsNext ? 'X' : 'O';
    }
      
    this.setState({
      squares: squares,
      xIsNext: !this.state.xIsNext,
      numTurns: this.state.numTurns + 1,
    });
  }

  renderSquare(i) {
    return (
      <Square
        value={this.state.squares[i]}
        onClick={() => this.handleClick(i)}
      />
    );
  }



  render() {
    const winner = calculateWinner(this.state.squares);
    let status;
    if (winner) {
      status = 'Winner: ' + winner;
    } else {
      status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
    }

    return (
      <div>
        <div className="status">{status}</div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-info">
          <div>{/* status */}</div>
          <ol>{/* TODO */}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
        
