import React, { Component } from "react";
import "./App.css";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import CebuloBoy from "./components/cebuloBoy";
import { Typography, IconButton } from "../node_modules/@material-ui/core";
import { RssFeed } from "@material-ui/icons";
import { GithubCircle, CodeBraces, Telegram } from "mdi-material-ui";

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <AppBar position="static" style={{ backgroundColor: "#1769aa" }}>
          <Toolbar>
            <img
              src={require("./gfx/cebulaboy-logo.png")}
              style={{
                width: 48,
                height: "auto",
                paddingRight: 10
              }}
              alt="CebuloBoy"
            />
            <Typography variant="headline" color="inherit">
              {" "}
              CebuloBoy{" "}
            </Typography>
            <IconButton
              href="/rss"
              style={{ position: "absolute", right: 0 }}
              aria-haspopup="true"
              color="inherit"
              target="_blank"
            >
              <RssFeed />
            </IconButton>
            <IconButton
              href="https://github.com/Behoston/CebuloBoy"
              target="_blank"
              style={{ position: "absolute", right: 50 }}
              aria-haspopup="true"
              color="inherit"
            >
              <GithubCircle />
            </IconButton>
            <IconButton
              href="/doc"
              style={{ position: "absolute", right: 100 }}
              aria-haspopup="true"
              color="inherit"
              target="_blank"
            >
              <CodeBraces />
            </IconButton>
            <IconButton
              href="https://t.me/armia_cebulo_boya"
              style={{ position: "absolute", right: 150 }}
              aria-haspopup="true"
              color="inherit"
              target="_blank"
            >
              <Telegram />
            </IconButton>
          </Toolbar>
        </AppBar>
        <CebuloBoy />
      </React.Fragment>
    );
  }
}

export default App;
