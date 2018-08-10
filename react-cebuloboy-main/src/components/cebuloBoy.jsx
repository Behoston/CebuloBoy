import React, { Component } from "react";
import { Typography, Paper } from "../../node_modules/@material-ui/core";
import PromotionGrid from "./promotionGrid";
import CountTo from "react-count-to";

class CebuloBoy extends Component {
  state = {
    promotions: [
      {
        name: "xkom",
        shop_gfx: require("../gfx/xkom-logo.png"),
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
        shop_gfx: require("../gfx/alto-logo.png"),
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
        shop_gfx: require("../gfx/morele-logo.png"),
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
        shop_gfx: require("../gfx/hardpc-logo.png"),
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
        shop_gfx: require("../gfx/komputronik-logo.png"),
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
        shop_gfx: require("../gfx/proline-logo.png"),
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
        <Typography align="center">
          <Paper square="true">
            Ile udało nam się zaoszczędzić:{" "}
            <CountTo
              to={this.state.promotions.money}
              speed={1000000000}
              delay={1}
            />{" "}
            zł
          </Paper>
        </Typography>
        {this.state.promotions.map((promotions, index) => (
          <PromotionGrid
            id={index}
            key={"promotionGrid_" + index}
            promotions={promotions}
            widths={this.state.widths}
          />
        ))}
      </React.Fragment>
    );
  }
}

export default CebuloBoy;
