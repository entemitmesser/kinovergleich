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
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
} from "@tanstack/react-table";
import React from "react";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { ArrowUpDown } from "lucide-react";

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

type Movie = {
  cinema_name: string;
  playtime_price: React.ReactNode;
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
    accessorKey: "playtime_price",
    header: "Spielzeiten & Preis",
  },
  {
    accessorKey: "cinema_name",
    header: "Ort",
  },
];

export default function MovieTable() {
  const movies = useQuery({
    queryFn: async () => {
      const result = await fetch("http://127.0.0.1:5000/movies");
      return movieData.parse(await result.json());
    },
    queryKey: ["movies"],
  });

  return (
    <div className="w-full">
      {movies.status === "pending" ? (
        "loading"
      ) : movies.status === "error" ? (
        <span className={"text-red-600"}>Error: {movies.error.message}</span>
      ) : (
        <DataTable
          columns={columns}
          data={movies.data.map((movie) => {
            return {
              title: movie.title,
              cinema_name: movie.location.name,
              playtime_price: JSON.parse(
                movie.playtime_price.replace(/'/g, '"'),
              ).map((item: string, index: number) => {
                return (
                  <div key={index}>
                    {item}
                    <br />
                  </div>
                );
              }),
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
}

export function DataTable<TData, TValue>({
  columns,
  data,
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
    <div className="w-full">
      <div className="flex items-center py-4">
        <Input
          placeholder="Filter nach Titel..."
          value={(table.getColumn("title")?.getFilterValue() as string) ?? ""}
          onChange={(event) =>
            table.getColumn("title")?.setFilterValue(event.target.value)
          }
          className="max-w-sm"
        />
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
                      {/* I removed the flexRender, because he was annoying nobody could answer me what he is doing */}
                      {cell.getContext().getValue() as Movie[keyof Movie]}
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
