import React, { Component } from "react";
import Promotion from "./cebuloBoy_promotion";
import "./cebuloBoy_promotion.css";
import {
  Grid,
  Paper,
  Typography,
  Divider
} from "../../node_modules/@material-ui/core";

class PromotionGrid extends Component {
  shopGfx() {
    if (this.props.promotions.name === "xkom") {
      return require("../gfx/xkom-logo.png");
    } else if (this.props.promotions.name === "alto") {
      return require("../gfx/alto-logo.png");
    } else if (this.props.promotions.name === "morele") {
      return require("../gfx/morele-logo.png");
    } else if (this.props.promotions.name === "hard-pc") {
      return require("../gfx/hardpc-logo.png");
    } else if (this.props.promotions.name === "komputronik") {
      return require("../gfx/komputronik-logo.png");
    } else if (this.props.promotions.name === "proline") {
      return require("../gfx/proline-logo.png");
    }
  }
  render() {
    return (
      <div style={{ padding: 20 }}>
        <Divider />
        <Paper
          elevation={1}
          classes={{
            root: "classes-state-root"
          }}
        >
          <Typography variant="display2" align="center">
            <Paper style={{ marginBottom: 5 }}>
              <img
                className="promotionImg"
                src={this.shopGfx()}
                alt={this.props.promotions.name}
              />
            </Paper>
          </Typography>
          <Grid
            container
            spacing={8}
            style={{ paddingLeft: 10, paddingRight: 10, paddingBottom: 10 }}
          >
            {this.props.promotions.last_promotions.map(
              (promotions, index) => (
                <Promotion
                  id={"promotion_" + index}
                  key={"promotion_" + index}
                  promotions={promotions}
                />
              )
            )}
          </Grid>
        </Paper>
      </div>
    );
  }
}

export default PromotionGrid;
