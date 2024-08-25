"use client";
import { z } from "zod";
import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import React from "react";
import { MovieCarousel } from "~/components/movie-carousel";
import { chunkArray } from "~/lib/utils";
import { Input } from "~/components/ui/input";
import { DatePicker } from "~/components/date-picker";

const movieData = z.array(
  z.object({
    poster_url: z.string(),
    title: z.string(),
    id: z.number(),
  }),
);

export type MovieData = z.infer<typeof movieData>;

export default function MoviePreviewShow() {
  const [date, setDate] = React.useState<Date>();
  const [title, setTitle] = React.useState<string>();
  const movies = useQuery({
    queryFn: async () => {
      const result = await fetch(
        date
          ? `http://127.0.0.1:5000/movies?date=${format(date.toString(), "dd-MM-yyyy")}`
          : "http://127.0.0.1:5000/movies",
      );
      return movieData.parse(await result.json());
    },
    queryKey: ["movies", date],
  });

  const filteredMovies =
    movies.data?.filter((movie) =>
      title ? movie.title.toLowerCase().includes(title.toLowerCase()) : true,
    ) ?? [];

  const movieChunks = chunkArray(filteredMovies, 10);

  return (
    <div className="flex w-full flex-col items-center gap-5">
      <div className="flex w-full gap-3 md:w-[90%]">
        <Input
          placeholder="Filter nach Titel..."
          value={title ?? ""}
          onChange={(event) => setTitle(event.target.value)}
          className="w-1/2 sm:w-72"
        />
        <DatePicker className="sm:w-auto" date={date} setDate={setDate} />
      </div>
      {movieChunks.map((chunk, index) => (
        <MovieCarousel
          key={index}
          loading={movies.isLoading}
          movieData={chunk}
        />
      ))}
    </div>
  );
}
