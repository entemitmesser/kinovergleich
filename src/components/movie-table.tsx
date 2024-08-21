"use client";
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";
import {
  type ColumnDef,
  type ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  type SortingState,
  useReactTable,
} from "@tanstack/react-table";
import React from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { ArrowUpDown } from "lucide-react";
import { DatePicker } from "./date-picker";
import { format } from "date-fns";
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

type Movie = {
  cinema_name: string;
  playtime_price: string;
  poster: string;
  title: string;
};

export const columns: ColumnDef<Movie>[] = [
  {
    accessorKey: "title",
    header: ({ column }) => {
      return (
        <Button
          variant="ghost"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Titel
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      );
    },
  },
  {
    accessorKey: "poster",
    header: "Poster",
    cell: ({ cell, row }) => {
      return (
        <div className="relative aspect-[7/10] w-40">
          <Image
            src={z.string().parse(cell.getValue())}
            alt={row.original.title + " Poster"}
            className="rounded"
            fill
          />
        </div>
      );
    },
  },
  {
    accessorKey: "playtime_price",
    header: "Spielzeiten & Preis",
    cell: ({ cell }) => {
      // Sanitize the JSON
      return z
        .array(z.string())
        .parse(JSON.parse(z.string().parse(cell.getValue()).replace(/'/g, '"')))
        .map((item: string, index: number) => {
          return (
            <div key={index}>
              {item}
              <br />
            </div>
          );
        });
    },
  },
  {
    accessorKey: "cinema_name",
    header: "Ort",
  },
];

export default function MovieTable() {
  const [date, setDate] = React.useState<Date>();
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

  return (
    <div className="w-full">
      {movies.status === "pending" ? (
        "loading"
      ) : movies.status === "error" ? (
        <span className={"text-red-600"}>Error: {movies.error.message}</span>
      ) : (
        <DataTable
          setDate={setDate}
          date={date}
          columns={columns}
          data={movies.data.map((movie) => {
            return {
              title: movie.title,
              cinema_name: movie.location.name,
              playtime_price: movie.playtime_price_formatted_json,
              poster: movie.poster_url,
            };
          })}
        ></DataTable>
      )}
    </div>
  );
}

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  date: Date | undefined;
  setDate: (type: Date | undefined) => void;
}

export function DataTable<TData, TValue>({
  columns,
  data,
  date,
  setDate,
}: DataTableProps<TData, TValue>) {
  const [columnFilters, setColumnFilters] = React.useState<ColumnFiltersState>(
    [],
  );
  const [sorting, setSorting] = React.useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    onColumnFiltersChange: setColumnFilters,
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    getSortedRowModel: getSortedRowModel(),
    state: {
      columnFilters,
      sorting,
    },
  });

  return (
    <div className="w-full p-6">
      <div className="flex items-center gap-4 py-4">
        <Input
          placeholder="Filter nach Titel..."
          value={(table.getColumn("title")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("title")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
        <DatePicker date={date} setDate={setDate} />
      </div>
      <div className="w-full rounded-md border">
        <Table className="w-full">
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext(),
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext(),
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
