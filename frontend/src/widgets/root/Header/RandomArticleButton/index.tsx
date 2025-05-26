import { Link } from "@tanstack/react-router";
import React from "react";
import QuestionMarkIcon from "./question-mark.svg?react";

const RandomArticleButton: React.FC = () => {
  return (
    <Link to="/article/random">
      <div className="wrapper">
        <QuestionMarkIcon />
      </div>
      Random article
    </Link>
  );
};

export default RandomArticleButton;
