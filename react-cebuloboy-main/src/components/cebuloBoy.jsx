import React, { Component } from "react";
import { Typography, Paper } from "../../node_modules/@material-ui/core";
import PromotionGrid from "./cebuloBoy_promotionGrid";
import CountUp from "react-countup";

class CebuloBoy extends Component {
  state = {
    money: { total: 0 },
    promotions: [],
  };
  componentDidMount() {
    fetch("http://gruzometr.pl:1337/last_promotions")
      .then(res => res.json())
      .then(result => {
        this.setState({ promotions: result });
      });
    fetch("http://gruzometr.pl:1337/saved_money")
      .then(res => res.json())
      .then(result => {
        this.setState({ money: result  });
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
              end={this.state.money.total}
              duration={30}
              redraw={true}
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
