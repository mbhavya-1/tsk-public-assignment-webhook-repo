import React from "react";
import EventList from "./EventList";
import "./App.css";

function App() {
  return (
    <div className="App">
      {/* Making the top heading */}
      <div className="header">
        <span id="companyName">
          <span id="Tech">Tech</span>
          <span id="StaX">StaX</span>
        </span>
        <span id="heading">: Developer Assessment Task</span>
      </div>
      {/* Displaying the github actions by using the EventList Component */}
      <EventList />
    </div>
  );
}

export default App;