"use client";
import { useState } from "react";

export default function LustigeListe() {
  const cities = [
    "keine",
    "ahnung",
    "ich",
    "bin",
    "zu",
    "faul",
    "hier",
    "städte",
    "rein",
    "zu",
    "schreiben",
  ];
  const [currentIndex, setCurrentIndex] = useState(-1);
  return (
    <>
      <h1>Liste</h1>
      <ul>
        {cities.map((item, index) => (
          <li
            key={index}
            className={
              currentIndex === index
                ? "active list-item bg-green-500"
                : "list-item"
            }
            onClick={() => {
              if (currentIndex == index) {
                setCurrentIndex(-1);
              } else {
                setCurrentIndex(index);
              }
            }}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}
