import * as React from "react";

import { Card, CardContent } from "~/components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "~/components/ui/carousel";
import { type MovieData } from "~/components/movie-show";
import Image from "next/image";
import { Skeleton } from "~/components/ui/skeleton";
import Link from "next/link";

export function MovieCarousel(
  props: { movieData: MovieData; loading: false } | { loading: true },
) {
  return (
    <Carousel className="w-full md:w-[90%]">
      <CarouselContent>
        {!props.loading
          ? props.movieData.map((movie, index) => (
              <CarouselItem
                key={index}
                className="basis-1/2 sm:basis-1/3 lg:basis-1/4 xl:basis-1/5"
              >
                <Link className="flex h-full p-1" href={`/movie/${movie.id}`}>
                  <Card className="flex-grow hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground">
                    <CardContent className="relative flex h-full w-full flex-col items-center justify-center gap-3 pt-6">
                      <div className="relative aspect-[7/10] w-full">
                        <Image
                          src={movie.poster_url}
                          alt={movie.title + " Poster"}
                          fill
                          className="rounded"
                        />
                      </div>
                      <div className="text-center text-base font-bold lg:text-xl">
                        {movie.title}
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              </CarouselItem>
            ))
          : Array.from({ length: 10 }).map((_, index) => (
              <CarouselItem key={index}>
                <div className="p-1">
                  <Card>
                    <CardContent className="aspect-[7/10] w-40">
                      <Skeleton className="h-full w-full" />
                    </CardContent>
                  </Card>
                </div>
              </CarouselItem>
            ))}
      </CarouselContent>
      <CarouselPrevious className="hidden md:flex" />
      <CarouselNext className="hidden md:flex" />
    </Carousel>
  );
}
