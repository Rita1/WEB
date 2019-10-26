// npm run watch
// source env/bin/activate
// export FLASK_APP=run.py
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
import Cookies from 'js-cookie';
import { Beforeunload } from 'react-beforeunload';

var $ = require('jquery');

function Field(props) {
  var bnt_class = 'square';
  var bState = '';
  if  (props.status.condition == 'FLAG') {
    bState = "F";
  }
  else if (props.status.condition != 'UNTOUCH') {
    bnt_class = 'square-clicked';
    bState = props.status.bomb_count;
  }
  return (
    <button id={props.i} className={bnt_class} onClick={props.onClick} onContextMenu={props.onContextMenu}>
      { bState }
    </button>
  );
}

// https://stackoverflow.com/questions/41978408/changing-style-of-a-button-on-click

class Board extends React.Component {

  constructor(props) {
    super(props);
  }

  renderField(x, y) {
    var i = this.return_index(x, y, this.props.cordX);
    // console.log("Fields from board", this.props.fields);
    return <Field i={i} status={this.props.fields[i]} onClick={() => this.props.onClick(i)}
    onContextMenu={(e) => this.props.onContextMenu(e, i)}/>;
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
        {this.renderBoardLines()}
      </div>
    );
  }
}

class NameForm extends React.Component {

  // user name
  // isRegister true if pressed StartGame
  // size: Small, Medium, Large
  // TODO user name, size
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

  // setCookie() {
  //   console.log("SetCookie");
  //   var today = new Date();
  //   Cookies.set('cookie', today);
  //   console.log("Cookies.get('cookie'),", Cookies.get('cookie'));
  // }

  // Enter name
  // Select size
  // Submit - Start game

  // Send everything to server
  // Get response - about active players
  //              - generated board with bombs
  // https://reactjs.org/docs/forms.html
  render() {
    return (
      <div>
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
      </div>
    );
  }
}

class GameInfo extends React.Component {

  render () {
    return (
      <div id="gameInfo">
        {this.props.userName && (<h2>Hello,  {this.props.userName}</h2>)}
        {this.props.gameOver && (<h1>BOOM!</h1>)}
        <h2>Active Players: {this.props.userCount}</h2>
      </div>
    );
  }
}

class Game extends React.Component {
    
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
      userCookie: Cookies.get('cookie'),
      userName: '',
      gameStart: false,
      gameOver: false,
      userCount : 0,
      size : "small",
      cordX : 0,
      cordY: 0,
      fields: [],
      oneTimeChecked: false,
      
    };

    this.eventSource = new EventSource("stream");
    this.handleSubmitForm = this.handleSubmitForm.bind(this);
    this.getDateCheckGameStatus = this.getDateCheckGameStatus.bind(this);
    this.handleUnload = this.handleUnload.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleRightClick = this.handleRightClick.bind(this);
  }

// https://www.jsdiaries.com/dynamic-website-design-with-event-source/
// https://stackoverflow.com/questions/25860304/how-do-i-set-response-headers-in-flask
// https://stackoverflow.com/questions/57241022/server-sent-events-not-receiving-messages-from-stream-with-react-and-nodejs

  componentDidMount() {
    if (! this.state.gameStart) {
       this.getDateCheckGameStatus();
    }
    console.log("from component did mountW");
    this.eventSource.onmessage = e => {
      console.log("kuku");
      console.log("Updating data", e.data);
    }
  }

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
      if (data) {
        //console.log(data)
        if (data.board) {
          if (data.board.fieldList){
            this.setState({
              fields : data.board.fieldList
            });
          }
          this.setState({
            cordX : data.board.cordX,
            cordY : data.board.cordY,
          });
        }
        if (data.gameStarted) {
          this.setState({
            gameStart : true,
          });
        }
        if (data.gameOver) {
          this.setState({
            gameOver : true,
          });
        }
        this.setState({
          userCount : data.userCount,
        });
      }
    });
    this.setState({
      oneTimeChecked: true,
    });
  }

  // Gets name, changes user name in state, passed to FORM
  handleSubmitForm (name, size) {
  
    var randomInt = Math.floor(Math.random() * 10000);
    this.setState({
      userName : name,
      gameStart: true,
      size: size,
      userCookie: randomInt,
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

  render() {
    
    console.log("State from Game render",this.state);
    // if (! this.state.gameStart) {
    //   this.getDateCheckGameStatus();
    // }
    return ( 
      <Beforeunload onBeforeunload={this.handleUnload}>
        <div className="game-board" key={1}>
          <GameInfo gameOver={this.state.gameOver} userCount={this.state.userCount} userName={this.state.userName}/>
          <NameForm sendData={this.handleSubmitForm} gameStarted={this.state.gameStart} />
          {this.state.userName && (! this.state.gameOver) && (
          <Board cordX={this.state.cordX} cordY={this.state.cordY} fields={this.state.fields} 
            onClick={(x, y) => this.handleClick(x, y)} 
            onContextMenu={(x,y) => this.handleRightClick(x, y)}/>
          )}
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