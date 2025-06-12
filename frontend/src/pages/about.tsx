import { PageHeading } from "@/shared/components";
import { Links } from "@/widgets/about";

const AboutPage = () => {
  return (
    <main>
      <div className="container">
        <PageHeading>About site</PageHeading>
        <p>
          Blogioma - project for education goals in Django, React, HTML and CSS.
          This project will be uploaded to GitHub for make Blogioma better and
          for experience in open source :D
        </p>

        <br />
        <br />
        <br />

        <Links />
      </div>
    </main>
  );
};

export default AboutPage;
