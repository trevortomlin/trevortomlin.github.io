/** @jsx h */

import blog, { ga, redirects, h } from "blog";

blog({
  title: "Trevor's Blog",
  description: "Anything computer science related",
  avatar: "images/headshot.png",
  avatarClass: "rounded-full",
  author: "Trevor Tomlin",
  links: [
    { title: "Email", url: "mailto:ttomlin2@comcast.net" },
    { title: "GitHub", url: "https://github.com/trevortomlin" },
    { title: "Linkedin", url: "https://www.linkedin.com/in/trevor-tomlin/" },
  ],
  lang: "en"
});
