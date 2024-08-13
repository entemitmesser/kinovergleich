"use client";
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";

const movieData = z.array(
  z.object({
    location: z.object({
      name: z.string(),
      url: z.string(),
    }),
    playtime_price: z.string(),
    title: z.string(),
  }),
);

export default function MovieTable() {
  const movies = useQuery({
    queryFn: async () => {
      const result = await fetch("http://127.0.0.1:5000/movies");
      return movieData.parse(await result.json());
    },
    queryKey: ["movies"],
  });

  return (
    <div>
      {movies.status === "pending" ? (
        "loading"
      ) : movies.status === "error" ? (
        <span className={"text-red-600"}>Error: {movies.error.message}</span>
      ) : (
        movies.data.map((movie) => <p>{movie.title}</p>)
      )}
    </div>
  );
}
