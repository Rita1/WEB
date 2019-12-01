
// https://github.com/angineering/fullstacktemplate
// https://www.youtube.com/watch?v=TKIHpoF8ZIk&feature=share&fbclid=IwAR16_T8Q-RhHQvxVGmCzlZgBlapyjDDU-1BZZaYJAe9rvrupmZUwGYf2HMU
// https://www.robinwieruch.de/webpack-babel-setup-tutorial/
// https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/
// https://www.npmjs.com/package/react-cookie
// https://reactjs.org/docs/testing-environments.html
// https://www.npmjs.com/package/react-beforeunload

// Game
// Board
// Field

// TODO Restart
// Calculate Winer

import React from 'react';
import ReactDOM from 'react-dom';
import { Beforeunload } from 'react-beforeunload';

var $ = require('jquery');

function Field(props) {
  var bnt_class = 'square-' + props.size;
  var bState = '';
  if  (props.status.condition == 'FLAG') {
    bState = "F";
  }
  else if (props.status.condition != 'UNTOUCH') {
    bnt_class = 'square-clicked-' + props.size;
    bState = props.status.bomb_count;
  }
  return (
    <button id={props.i} className={bnt_class} onClick={props.onClick} onContextMenu={props.onContextMenu}>
      { bState }
    </button>
  );
}

// https://stackoverflow.com/questions/41978408/changing-style-of-a-button-on-click
// https://developmentarc.gitbooks.io/react-indepth/content/life_cycle/birth/component_render.html
// https://stackoverflow.com/questions/33075063/what-is-the-exact-usage-of-componentwillupdate-in-reactjs/33075514#33075514
  // After bom, shows boom and sleeps 3 second
  // https://stackoverflow.com/questions/30803440/delayed-rendering-of-react-components

class Board extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      hidden : true,
      wait : 3000,
    }  
  }

  show() {
    this.setState({hidden : false});
  }

  componentWillMount() {
    var that = this;
    if (this.props.gameOver === true) {
      setTimeout(function() {
        that.show();
      }, this.state.wait);
    }
    else {
      this.setState({hidden : false});
    }
  }

  componentWillReceiveProps(nextProps){
    if (nextProps.gameOver === true){
      this.setState({hidden : true})
    }
  }

  componentWillUpdate(newProps,newState) {
    var that = this;
    if (this.props.gameOver === true) {
      setTimeout(function() {
        that.show();
      }, this.state.wait);
    }
  }

  renderField(x, y) {
    var i = this.return_index(x, y, this.props.cordX);
    return <Field i={i} status={this.props.fields[i]} onClick={() => this.props.onClick(i)}
    onContextMenu={(e) => this.props.onContextMenu(e, i)} size={this.props.size}/>;
  }

  renderBoardCol(y) {

    var x = this.props.cordX;
    var col = [];
    var n;
    for (n = 0; n < x; n++) {
      col.push(<div className="board-col" key={n}>{this.renderField(n, y)}</div>);
    }
    return col;
  }

  // x size, y size
  // return list of fields: rows    - <div></div>
  //                        squares - <div> of buttons <div>
  renderBoardLines() {

    var y = this.props.cordY;
    var lines = [];
    var i;
    for (i = 0; i < y; i++) {
      lines.push(<div className="board-row" key={i}>
      {this.renderBoardCol(i)}</div>);
    }
    return lines;
  }

  // Helper method calculate Index
  
  return_index(x, y, CordX) {
    var index = (y * CordX) + x;
    return index
  }

  render () {
    // https://revs.runtime-revolution.com/react-passing-data-between-components-with-pokemon-as-an-example-ac2b5ab59b26
    // https://codepen.io/gaearon/pen/aWWQOG?editors=0010
    return (
      
      <div>
        {this.state.hidden && (<h1>BOOM!!!</h1>)}
        {!this.state.hidden && (this.renderBoardLines())}
      </div>  
    );
  }
}

class NameForm extends React.Component {

  // user name
  // isRegister true if pressed StartGame
  // size: Small, Medium, Large

  constructor(props) {
    super(props);
    this.state = {
      userName: '',
      //userCookie: '',
      isRegister: false,
      size: 'small',
    
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }



  handleChange(event) {

    const target = event.target;
    const value = target.value;
    const name = target.name;
    this.setState({
      [name]: value,
    });
  }

  handleSubmit(event) {

    if (this.state.userName) {
      this.props.sendData(this.state.userName, this.state.size);
      // this.setCookie();
       this.setState({
         isRegister: true,
       });
    }
    else {
      alert("Please fill Your name!");
    }
    event.preventDefault();
  }

  // Enter name
  // Select size
  // Submit - Start game

  // Send everything to server
  // Get response - about active players
  //              - generated board with bombs
  // https://reactjs.org/docs/forms.html
  render() {
    return (
      <div class="form-group">
        {!this.state.isRegister && !this.props.gameStarted && (
        <form onSubmit={this.handleSubmit}>
          <label>
            User Name:
            <input name="userName" type="text" value={this.state.userName} onChange={this.handleChange} />
          </label>
          <br />
          <label>
            Select size:
            <select name="size" value={this.state.size} onChange={this.handleChange}>
              <option value="small">Small</option>
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </label>
          <input type="submit" value="Start Game" />
        </form>
        )}
        {!this.state.isRegister && this.props.gameStarted && (
          <form onSubmit={this.handleSubmit}>
            <label>
              User Name:
              <input name="userName" type="text" value={this.state.userName} onChange={this.handleChange} />
            </label>
            <br />
            <input type="submit" value="Start Game" />
          </form>
        )}
        {this.state.isRegister && !this.props.gameStarted && (
          <form onSubmit={this.handleSubmit}>
            <label>
              Select size:
              <select name="size" value={this.state.size} onChange={this.handleChange}>
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
              </select>
              </label>
              <br />
              <input type="submit" value="Start Game" />
          </form>
        )}
      </div>
    );
  }
}

class GameInfo extends React.Component {

  constructor(props) {
    super(props)
    this.renderUsers = this.renderUsers.bind(this)
  }

  userItem(user) {
    return (
    <tr>
      <td>{user["username"]}</td>
      <td>{user["total_qty"]}</td>
    </tr>
    );
  }

// https://stackoverflow.com/questions/50862192/react-typeerror-cannot-read-property-props-of-undefined
// https://reactjs.org/docs/lists-and-keys.html
  renderUsers (users) {
    var userLines = [];
    if (users) {
      Object.keys(users).forEach(function(key) {
        userLines.push(users[key])
      });
    }
    return (
      <table id="table" className="table table-striped">
      <thead>
        <tr>
          <th>Name</th>
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
          {userLines.map((u) =>
            this.userItem(u)
          )}
      </tbody>
      </table>
    )
  };

  render () {
    return (
      <div id="gameInfo">
        {this.props.gameWin && 
            <h1> Winner is - {this.props.gameWinUser} </h1>
          }
        {this.props.gameWin &&
          (<button type="button" className="btn btn-dark" onClick={this.props.onClickRestart}>
            Restart Game
          </button>)}
        {!this.props.gameWin &&   
        <h2>Active Players:
           {this.props.userCount}</h2>}
        {this.renderUsers(this.props.users)}
      </div>
    );
  }
}

// (this.state.xIsNext ? "X" : "O")

// {this.props.gameWin &&  
//   (<button type="button" class="btn btn-dark" onClick={this.props.onClickRestart}>
//     Restart Game
//   </button>)}

class Game extends React.Component {
  // 
  // 1. Choose size - buttons
  //     pass size to board functions
  // 2. Create board by what size
  // 3. Count active players
  // 4. Get from server info about mines and mines count
  // 4. Players dig on field
  // 5. flag
  // 6. unflag
  // 7. ...
  
  constructor(props) {
    super(props);
    this.state = {
      name : '',
      userCookie: '',
      userName: '',
      gameStart: false,
      gameOver: false,
      userCount : 0,
      size : "small",
      cordX : 0,
      cordY: 0,
      fields: [],
      oneTimeChecked: false,
      gameWin: false,
      gameWinUser: 'Unknown',
      users: '',
      
    };

    this.eventSource = new EventSource("stream");
    this.handleSubmitForm = this.handleSubmitForm.bind(this);
    this.getDateCheckGameStatus = this.getDateCheckGameStatus.bind(this);
    this.handleUnload = this.handleUnload.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleRightClick = this.handleRightClick.bind(this);
    this.onClickRestart = this.onClickRestart.bind(this);
  }

// https://www.jsdiaries.com/dynamic-website-design-with-event-source/
// https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask
// https://stackoverflow.com/questions/57241022/server-sent-events-not-receiving-messages-from-stream-with-react-and-nodejs

  componentDidMount() {
    if (! this.state.gameStart) {
       this.getDateCheckGameStatus();
    }
    this.eventSource.onmessage = e => {
      var data = $.parseJSON(e.data)
      this.processData(data)
    }
  }

  processData(data) {
    if (data) {
      if (data.board) {
        if (data.board.fieldList){
          this.setState({
            fields : data.board.fieldList
          });
        }
        this.setState({
          cordX : data.board.cordX,
          cordY : data.board.cordY,
          size : data.board.size,
        });
      }
      if (!data.board) {
        this.setState({
          gameStart : false,
          // fields : [],
        })
      }
      if (data.gameStarted) {
        this.setState({
          gameStart : true,
        });
      }
      console.log("data.gameOver, this.state.userCookie", data.gameOver, this.state.userCookie)
      if (data.gameOver == this.state.userCookie) {
        this.setState({
          gameOver : true,
        });
      }
      if (!data.gameOver || data.gameOver != this.state.userCookie) {
        this.setState({
          gameOver : false,
        });
      }
      if (data.board && data.board.gameWin) {
        this.setState({
          gameWin : data.board.gameWin,
          gameWinUser : data.gameWinUser,
        });
      }
      if (data.board && !data.board.gameWin) {
        this.setState({
          gameWin : false,
          gameWinUser : '',
        });
      }
      this.setState({
        userCount : data.userCount,
        users : data.users,
      });
    }
  this.setState({
    oneTimeChecked: true,
  });
};

  getData(toSend) {
    if (! toSend) {
      toSend = {}
    }
    var fromState = {};
    var fullData = {};

    fromState.userCookie = this.state.userCookie;
    fromState.userName = this.state.userName;
    fromState.size = this.state.size;

    fullData = Object.assign(toSend, fromState);
    $.get(window.location.href + 'board', fullData, (data) => {
      this.processData(data);
    });
  }

  // Gets name, changes user name in state, passed to FORM
  handleSubmitForm (name, size) {
    
    var cookie = this.state.userCookie;
    if (!cookie) {
      var cookie = Math.floor(Math.random() * 10000);
    };
    this.setState({
      userName : name,
      gameStart: true,
      size: size,
      userCookie: cookie,
    }, () => {
      this.getData();
    });
  }

  // Send Left and right click info to server
  handleClick (i) {
    // console.log("Handle click")
    this.getData( { action : 'dig', id : i } )
  }

  handleRightClick(e, i) {
    // console.log("Right click")
    e.preventDefault();
    this.getData( { action : 'flag', id : i } )
  }
  // Send to server, when window is closed
  handleUnload () {
    // console.log("Status unload")
    this.getData( { logout : true } )
  } 

  // Patikrinam ar prasidejes zaidimas serveryje:
  // Jeigu ne:
  //   Liepiam registruotis
  //   Kai uzsiregistruoja , persiunciam info i serveri ir gaunam duomenis
  // Jeigu taip:
  //   Liepiam registruotis, bet neduodam pasirinkti dydzio

  getDateCheckGameStatus() {
    // console.log("Status check")
    if ( ! this.state.oneTimeChecked ) {
        this.getData( { checkStart : true } )
    }    
  }

  onClickRestart() {

    this.getData( { restart : true } )

  }

  render() {
    var boardClass = 'game-board-' + this.state.size
    console.log("State from Game render, boardClass",this.state, boardClass);
    return ( 
      <Beforeunload onBeforeunload={this.handleUnload}>
        <div className="container">
          <div className={boardClass} key={1}>
            <NameForm sendData={this.handleSubmitForm} gameStarted={this.state.gameStart} />
            {this.state.userName && this.state.gameStart && !this.state.gameWin && (
              <Board cordX={this.state.cordX} cordY={this.state.cordY} fields={this.state.fields} 
                onClick={(x, y) => this.handleClick(x, y)} 
                onContextMenu={(x,y) => this.handleRightClick(x, y)}
                gameOver={this.state.gameOver} size={this.state.size}/>
              )}
          </div>
         <div className="game-info" key={2}>
            <GameInfo userCount={this.state.userCount} userName={this.state.userName} 
              gameWin={this.state.gameWin} users={this.state.users}
              gameWinUser={this.state.gameWinUser}
              onClickRestart={() => this.onClickRestart()}/>
          </div>
        </div>
      </Beforeunload>
    );
  }
}

ReactDOM.render(
    <Game />,
  document.getElementById('root')
);
// https://auth0.com/blog/developing-real-time-web-applications-with-server-sent-events/