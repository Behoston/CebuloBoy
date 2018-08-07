import React, { Component } from "react";
import "./promotion.css";
import {
  Grid,
  Card,
  Button,
  Typography,
  CardContent,
  CardActions,
  Divider
} from "../../node_modules/@material-ui/core";
import LinkPreview from "react-native-link-preview";

class Promotion extends Component {
  componentDidMount() {
    // console.log(this.props.promotions);
  }
  getItemImg() {
    const preview = LinkPreview.getPreview(this.props.promotions.url);
    preview.then(result => {
      return result.images[result.images.length - 1];
    });
  }
  fixDigits() {
    let price =
      this.props.promotions.old_price - this.props.promotions.new_price;
    price = price.toFixed(2);
    return price;
  }
  getPercent() {
    let percent =
      ((this.props.promotions.old_price - this.props.promotions.new_price) /
        this.props.promotions.old_price) *
      100;
    percent = percent.toFixed(0);
    return percent;
  }
  promoCode() {
    if (
      this.props.promotions.code !== "" &&
      this.props.promotions.code !== null &&
      this.props.promotions.code !== undefined
    ) {
      return "Kod do promocji: " + this.props.promotions.code;
    } else {
      return "";
    }
  }
  wchichShop() {}

  render() {
    const {
      product_name,
      old_price,
      new_price,
      url,
      shop_gfx
    } = this.props.promotions;
    console.log(this.props.promotions);
    return (
      <Grid xs={this.props.widths}>
        <Card className="promotionCard">
          <Divider />

          <Typography align="center">
            <img
              className="promotionMedia"
              title={product_name}
              src={this.getItemImg()}
              alt=""
            />
          </Typography>
          <CardContent>
            <Divider />
            <Typography variant="subheading">{product_name}</Typography>
            <Typography component="p">
              Cena <s>{old_price}</s> zł -> {new_price}
            </Typography>
            <Typography component="p">
              Taniej o {this.fixDigits()} zł ({this.getPercent()}%)
            </Typography>
            <Typography component="p">{this.promoCode()}</Typography>
            <CardActions>
              <Button
                align="center"
                variant="contained"
                size="small"
                style={{ backgroundColor: "#1769aa", color: "white" }}
                href={url}
                target="_blank"
              >
                Link do promocji
              </Button>
            </CardActions>
          </CardContent>
        </Card>
      </Grid>
    );
  }
}

export default Promotion;
