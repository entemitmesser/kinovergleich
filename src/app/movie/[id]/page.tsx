"use client";
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";
import Link from "next/link";
import { useState } from "react";
import { Link as LinkIcon } from "lucide-react";
import Image from "next/image";

const movieData = z.array(
  z.object({
    location: z.object({
      name: z.string(),
      url_website_cinema: z.string(),
    }),
    poster_url: z.string(),
    playtime_price_formatted_json: z.string(),
    title: z.string(),
  }),
);

export default function Page({ params }: { params: { id: string } }) {
  const movie = useQuery({
    queryFn: async () => {
      const result = await fetch(`http://127.0.0.1:5000/movie?id=${params.id}`);
      return movieData.parse(await result.json());
    },
    queryKey: ["movie", params.id],
  });

  const [seeMore, setSeeMore] = useState(false);

  return (
    <>
      {movie.status === "pending" ? (
        "Loading..."
      ) : movie.status === "error" || !movie.data?.[0] ? (
        "Error"
      ) : (
        <div className="flex">
          <div className="flex flex-col gap-3">
            <span>Titel: {movie.data[0].title}</span>
            <span className="flex gap-1.5">
              Kino:{" "}
              <Link
                className="flex items-center gap-1.5 underline"
                href={movie.data[0].location.url_website_cinema}
              >
                {movie.data[0].location.name} <LinkIcon className="h-5 w-5" />
              </Link>
            </span>
            <div>
              Preise:{" "}
              <button onClick={() => setSeeMore((prevState) => !prevState)}>
                {seeMore ? "Weniger anzeigen" : "Mehr anzeigen"}
              </button>
              {seeMore
                ? z
                    .array(z.string())
                    .parse(
                      JSON.parse(
                        z
                          .string()
                          .parse(movie.data[0].playtime_price_formatted_json)
                          .replace(/'/g, '"'),
                      ),
                    )
                    .map((item: string, index: number) => {
                      return (
                        <div key={index}>
                          {item}
                          <br />
                        </div>
                      );
                    })
                : null}
            </div>
          </div>
          <div className="relative aspect-[7/10] h-64 md:h-96">
            <Image
              src={movie.data[0].poster_url}
              alt={movie.data[0].title + " Poster"}
              fill
            />
          </div>
        </div>
      )}
    </>
  );
}
