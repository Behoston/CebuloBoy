import React, { Component } from "react";
import "./App.css";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import {
  Typography,
  IconButton,
  Paper,
  SvgIcon
} from "../node_modules/@material-ui/core";
import { AccountCircle, RssFeed } from "@material-ui/icons";
import { GithubCircle, CodeBraces, Telegram } from "mdi-material-ui";

import PromotionGrid from "./components/promotionGrid";
import CountTo from "react-count-to";

class App extends Component {
  state = {
    promotions: [
      {
        name: "xkom",
        shop_gfx: require("./gfx/xkom-logo.png"),
        last_promotions: [
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          }
        ]
      },
      {
        name: "alto",
        shop_gfx: require("./gfx/alto-logo.png"),
        last_promotions: [
          {
            product_name: "string",
            old_price: 39,
            new_price: 29,
            url: "https://al.to/goracy_strzal/15272",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 200,
            new_price: 50,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          }
        ]
      },
      {
        name: "morele",
        shop_gfx: require("./gfx/morele-logo.png"),
        last_promotions: [
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          }
        ]
      },
      {
        name: "hard-pc",
        shop_gfx: require("./gfx/hardpc-logo.png"),
        last_promotions: [
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          }
        ]
      },
      {
        name: "komputronik",
        shop_gfx: require("./gfx/komputronik-logo.png"),
        last_promotions: [
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          },
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",
            gfx: ""
          }
        ]
      },
      {
        name: "proline",
        shop_gfx: require("./gfx/proline-logo.png"),
        last_promotions: [
          {
            product_name: "string",
            old_price: 0,
            new_price: 0,
            url: "https://x-kom.pl/goracy_strzal/15274",
            code: "",

            gfx: ""
          }
        ]
      }
    ],
    widths: [2, 2, 2, 2, 2, 2],
    money: "21312421421"
  };

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
            >
              <CodeBraces />
            </IconButton>
            <IconButton
              href="https://t.me/armia_cebulo_boya"
              style={{ position: "absolute", right: 150 }}
              aria-haspopup="true"
              color="inherit"
            >
              <Telegram />
            </IconButton>
          </Toolbar>
        </AppBar>
        <Typography align="center">
          <Paper square="true">
            Ile udało nam się zaoszczędzić:{" "}
            <CountTo to={92332424} speed={1000000000} delay={1} /> zł
          </Paper>
        </Typography>

        {this.state.promotions.map(
          (promotions, index) => (
            <PromotionGrid
              id={index}
              key={"promotionGrid_" + index}
              promotions={promotions}
              widths={this.state.widths}
            />
          )
          // console.log(promotions, index)
        )}
      </React.Fragment>
    );
  }
}

export default App;
