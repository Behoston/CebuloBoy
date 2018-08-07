import React, { Component } from "react";
import Promotion from "./promotion";
import "./promotion.css";

import {
  Grid,
  Paper,
  Typography,
  Divider
} from "../../node_modules/@material-ui/core";
import LinkPreview from "react-native-link-preview";

class PromotionGrid extends Component {
  componentDidMount() {
    // console.log(this.props.shop);
    // const promotions = this.state.promotions.map((element, index) => {
    //   console.log(element.last_promotions[0].url);
    //   return LinkPreview.getPreview(element.last_promotions[0].url).then(
    //     data => {
    //       const gfx = data.images[data.images.length - 1];
    //       return { ...element, gfx };
    //     }
    //   );
    // });
    // Promise.all(promotions).then(promotions => {
    //   this.setState({ promotions });
    //   // console.log(this.state);
    // });
    // console.log(this.props.promotions.last_promotions);
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
                src={this.props.promotions.shop_gfx}
                alt=""
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
                  widths={this.props.widths[index]}
                />
              )
              // console.log(promotions, index)
            )}
          </Grid>
        </Paper>
      </div>
    );
  }
}

export default PromotionGrid;
