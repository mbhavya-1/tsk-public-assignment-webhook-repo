import React, { useEffect, useState } from "react";
import axios from "axios";

const EventList = () => {
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    try {
      const response = await axios.get("http://localhost:5000/webhook/get-updates"); // Replace with your ngrok if needed
      setEvents(response.data.reverse()); // newest first
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
      <h2>Latest GitHub Events</h2>
      <ul>
        {events.map((event, index) => (
          <li key={index}>{formatMessage(event)}</li>
        ))}
      </ul>
    </div>
  );
};

export default EventList;