import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const EventList = () => {

  // useState hook is used to continuously update events every 15 secs
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    try {

      // axios is used to fetch data from backend
      const response = await axios.get("http://localhost:5000/webhook/get-updates");
      setEvents(response.data);
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };

  useEffect(() => {
    fetchEvents(); // initial load
    const interval = setInterval(fetchEvents, 15000); // refresh every 15s

    return () => clearInterval(interval); // clean up
  }, []);

  const formatMessage = (event) => {
    const timestamp = new Date(event.timestamp).toUTCString();

    // Aligning the data for UI output
    switch (event.action) {
      case "PUSH":
        return `"${event.author}" pushed to "${event.from_branch}" on ${timestamp}`;
      case "PULL REQUEST":
        return `"${event.author}" submitted a pull request from "${event.from_branch}" to "${event.to_branch}" on ${timestamp}`;
      case "MERGE":
        return `"${event.author}" merged branch "${event.from_branch}" to "${event.to_branch}" on ${timestamp}`;
      default:
        return "Unknown event";
    }
  };

  return (
    <div>
        <h2 className="semiHeading">Github Actions (Push/Post/Merge) on "action-repo"</h2>
        <ul className="content">
          {/* looping over the events list and displaying all the events (github actions) as a list */}
          {events.map((event, index) => (
            <li className="item" key={index}>{formatMessage(event)}</li>
          ))}
        </ul>
      </div>
  );
};

export default EventList;