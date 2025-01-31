/*
We're constantly improving the code you see. 
Please share your feedback here: https://form.asana.com/?k=uvp-HPgd3_hyoXRBw1IcNg&d=1152665201300829
*/

import PropTypes from "prop-types";
import React from "react";
import "./style.css";

export const ShowChart = ({ className, showChart = "/img/show-chart.png" }) => {
  return (
    <img
      className={`show-chart ${className}`}
      alt="Show chart"
      src={showChart}
    />
  );
};

ShowChart.propTypes = {
  showChart: PropTypes.string,
};
