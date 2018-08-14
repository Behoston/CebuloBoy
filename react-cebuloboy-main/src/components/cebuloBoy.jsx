import React, { Component } from "react";
import { Typography, Paper } from "../../node_modules/@material-ui/core";
import PromotionGrid from "./cebuloBoy_promotionGrid";
import CountUp from "react-countup";

class CebuloBoy extends Component {
  state = {
    money: 15423,
    promotions: []
  };
  componentDidMount() {
    fetch("https://cors.io/?https://propaniusz.tk/test.json?format=json")
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
            <CountUp
              delay={5}
              start={0}
              prefix="Ile udało nam się zaoszczędzić: "
              suffix=" zł"
              end={this.state.money}
              duration={30}
            />
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
