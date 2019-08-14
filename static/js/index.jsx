// npm run watch
// source env/bin/activate
// export FLASK_APP=run.py
// https://github.com/angineering/fullstacktemplate
// https://www.youtube.com/watch?v=TKIHpoF8ZIk&feature=share&fbclid=IwAR16_T8Q-RhHQvxVGmCzlZgBlapyjDDU-1BZZaYJAe9rvrupmZUwGYf2HMU
// https://www.robinwieruch.de/webpack-babel-setup-tutorial/
// https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/
// https://www.npmjs.com/package/react-cookie
// https://reactjs.org/docs/testing-environments.html

// Game
// Board
// Field

// TODO Restart
// Calculate Winer

import React from 'react';
import ReactDOM from 'react-dom';
//import Cookies from 'js-cookie';

var $ = require('jquery');

function Field() {
  return (
    <button className="square" >
      !
    </button>
  );
}

class Board extends React.Component {

  constructor(props) {
    super(props);
  }

  renderField() {
    return <Field />;
  }

  renderBoardCol() {

    var x = this.props.cordX;
    var col = [];
    var n;
    for (n = 0; n < x; n++) {
      col.push(<div className="board-col" key={n}>{this.renderField()}</div>);
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
      {this.renderBoardCol()}</div>);
    }
    return lines;
  }

  render () {
    console.log("CordX", this.props.cordX);
    console.log("CordY", this.props.cordY);
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
  constructor(props) {
    super(props);
    this.state = {
      userName: '',
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

    // Todo, dont let submit if username is empty

    this.props.sendData(this.state.userName,this.state.size);
    this.setState({
      isRegister: true,
    });
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
      <div>
        {this.state.isRegister && (<h2>Hy {this.state.userName}</h2>)};
        {!this.state.isRegister && (
        <form onSubmit={this.handleSubmit}>
          <label>
            Name:
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
   //   userCookies: Cookies.get('username'),
      userName: '',
      isRegister: false,
      userCount : 0,
      size : "small",
      cordX : 4,
      cordY: 5,
    };
    
    this.handleSubmitForm = this.handleSubmitForm.bind(this);
    this.getData = this.getData.bind(this);
  }
    
  getData() {

    if (this.state.isRegister) {
      $.get(window.location.href + 'board', { userName: this.state.userName,  size: this.state.size}, (data) => {
        var jsonData = JSON.parse(data);
        this.setState({
          userCount : jsonData.userCount,
          cordX : jsonData.board.cordX,
          cordY : jsonData.board.cordY,
        });
      });
    }
  }

  // Gets name, changes user name in state, passed to FORM
  handleSubmitForm (name, size) {

    this.setState({
      userName : name,
      isRegister: true,
      size: size,
    }, () => {
      this.getData();
    });
  }

  render() {
    
    console.log("State from Game render",this.state);
    return ( 
      <div className="game-board" key={1}>
        <h2>Active Players: {this.state.userCount}</h2>
        <NameForm sendData={this.handleSubmitForm}/>
        <Board cordX={this.state.cordX} cordY={this.state.cordY}/>
      </div>
    );
  }
}

ReactDOM.render(
    <Game />,
  document.getElementById('root')
);


// https://vladimirponomarev.com/blog/authentication-in-react-apps-creating-components
// https://serverless-stack.com/chapters/create-a-login-page.html?fbclid=IwAR0nx5eyiCZQltAFqvF1OQ_jte78lKFK54bD-zp1GcywYXW8tXzBb-386Pc
// https://stackoverflow.com/questions/51109559/get-cookie-with-react