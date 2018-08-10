import React, { Component } from "react";
import { Typography, Paper } from "../../node_modules/@material-ui/core";
import PromotionGrid from "./cebuloBoy_promotionGrid";
import CountTo from "react-count-to";

class CebuloBoy extends Component {
  state = {
    money: 21312421421,
    promotions: []
  };
  componentDidMount() {
    fetch("http://projekty.propanek.tk/test/test.json")
      .then(res => res.json())
      .then(result => {
        this.setState({ promotions: result.promotion });
      });
  }
  render() {
    return (
      <React.Fragment>
        <Paper square={true}>
          <Typography align="center">
            Ile udało nam się zaoszczędzić:{" "}
            <CountTo to={this.state.money} speed={1000000000} delay={1} /> zł
          </Typography>
        </Paper>
        {this.state.promotions.map((promotions, index) => (
          <PromotionGrid
            id={index}
            key={"promotionGrid_" + index}
            promotions={promotions}
          />
        ))}
      </React.Fragment>
    );
  }
}

export default CebuloBoy;
