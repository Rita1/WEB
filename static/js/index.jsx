// npm run watch
// source env/bin/activate
// export FLASK_APP=server/server.py
// https://github.com/angineering/fullstacktemplate
// https://www.youtube.com/watch?v=TKIHpoF8ZIk&feature=share&fbclid=IwAR16_T8Q-RhHQvxVGmCzlZgBlapyjDDU-1BZZaYJAe9rvrupmZUwGYf2HMU
// https://www.robinwieruch.de/webpack-babel-setup-tutorial/
// https://linoxide.com/linux-how-to/setup-python-virtual-environment-ubuntu/

import React from 'react';
import ReactDOM from 'react-dom';

var $ = require('jquery');
//alert(“Hello World!”);

class Class1 extends React.Component {

    constructor(props) {
      super(props);
      this.state = {
        name : "Name from class1"
      };
      this.getData();
    }
    
    getData() {
      console.log("1");
      $.get(window.location.href + 'board', (data) => {
          console.log(data);
          this.setState({
              name : data,
        });
      });
    }

    render() {

        return (
          <div>
            <h2> Test from js render </h2>
            <h1>{this.state.name}</h1>
          </div>
        );
      }
    }

ReactDOM.render(
    <Class1 />,
    
    document.getElementById('root')
  );
console.log("KUKU");