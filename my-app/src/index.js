import React,{useState} from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import App from "./App";

const root = ReactDOM.createRoot(document.getElementById("root")); 

root.render(
    <>
      <App/>
    </>
  );