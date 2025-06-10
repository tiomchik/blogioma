import { Article } from "@/app/types";
import { Button, Pfp } from "@/shared/components";
import { Link } from "@tanstack/react-router";
import React from "react";
import { formatDate, truncateWithEllipsis } from "./utils";
import "./index.scss";

type Props = Omit<Article, "viewings">;

const ArticleCard: React.FC<Props> = ({
  id,
  heading,
  full_text,
  author,
  pub_date,
  update,
}) => {
  const date = new Date(update ? update : pub_date);

  return (
    <article className="article">
      <h1>{truncateWithEllipsis(heading, 60)}</h1>
      <p>{truncateWithEllipsis(full_text, 110)}</p>

      <div className="author">
        <Link
          to="/profile/$username"
          params={{ username: author.username }}
          className="user"
        >
          <Pfp pfp={author.pfp} />
          {truncateWithEllipsis(author.username, 20)}
        </Link>
        <Link to="/article/$pk" params={{ pk: id.toString() }}>
          <Button>Read</Button>
        </Link>
      </div>

      {update ? (
        <p className="date">{"Updated: " + formatDate(date)}</p>
      ) : (
        <p className="date">{"Published: " + formatDate(date)}</p>
      )}
    </article>
  );
};

export default ArticleCard;
