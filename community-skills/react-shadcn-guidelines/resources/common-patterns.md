# Common Patterns

Frequently used patterns for forms, authentication, tables, dialogs, and other common UI elements with shadcn/ui and Tailwind CSS.

---

## Authentication with useAuth

### Getting Current User

```typescript
import { useAuth } from '@/hooks/useAuth';

export const MyComponent: React.FC = () => {
    const { user } = useAuth();

    // Available properties:
    // - user.id: string
    // - user.email: string
    // - user.username: string
    // - user.roles: string[]

    return (
        <div className="space-y-2">
            <p className="text-sm text-muted-foreground">
                Logged in as: {user.email}
            </p>
            <p className="text-sm">Username: {user.username}</p>
            <p className="text-sm">Roles: {user.roles.join(', ')}</p>
        </div>
    );
};
```

**NEVER make direct API calls for auth** - always use `useAuth` hook.

---

## Forms with React Hook Form + shadcn

### Basic Form with shadcn Form Components

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

// Zod schema for validation
const formSchema = z.object({
    username: z.string().min(3, 'Username must be at least 3 characters'),
    email: z.string().email('Invalid email address'),
    age: z.coerce.number().min(18, 'Must be 18 or older'),
});

type FormData = z.infer<typeof formSchema>;

export const MyForm: React.FC = () => {
    const { toast } = useToast();

    const form = useForm<FormData>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            username: '',
            email: '',
            age: 18,
        },
    });

    const onSubmit = async (data: FormData) => {
        try {
            await api.submitForm(data);
            toast({
                title: "Success",
                description: "Form submitted successfully",
            });
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to submit form",
                variant: "destructive",
            });
        }
    };

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <FormField
                    control={form.control}
                    name="username"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Username</FormLabel>
                            <FormControl>
                                <Input placeholder="Enter username" {...field} />
                            </FormControl>
                            <FormDescription>
                                Your public display name
                            </FormDescription>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Email</FormLabel>
                            <FormControl>
                                <Input type="email" placeholder="Enter email" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <FormField
                    control={form.control}
                    name="age"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Age</FormLabel>
                            <FormControl>
                                <Input type="number" placeholder="Enter age" {...field} />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <Button type="submit" className="w-full">
                    Submit
                </Button>
            </form>
        </Form>
    );
};
```

### Alternative: Manual Form (Without shadcn Form)

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

const formSchema = z.object({
    email: z.string().email('Invalid email'),
    password: z.string().min(8, 'Password must be at least 8 characters'),
});

type FormData = z.infer<typeof formSchema>;

export const LoginForm: React.FC = () => {
    const { toast } = useToast();
    const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
        resolver: zodResolver(formSchema),
    });

    const onSubmit = async (data: FormData) => {
        try {
            await api.login(data);
            toast({
                title: "Success",
                description: "Logged in successfully",
            });
        } catch (error) {
            toast({
                title: "Error",
                description: "Invalid credentials",
                variant: "destructive",
            });
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                    id="email"
                    type="email"
                    {...register('email')}
                    className={errors.email ? 'border-destructive' : ''}
                />
                {errors.email && (
                    <p className="text-sm text-destructive">{errors.email.message}</p>
                )}
            </div>

            <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <Input
                    id="password"
                    type="password"
                    {...register('password')}
                    className={errors.password ? 'border-destructive' : ''}
                />
                {errors.password && (
                    <p className="text-sm text-destructive">{errors.password.message}</p>
                )}
            </div>

            <Button type="submit" className="w-full">
                Log In
            </Button>
        </form>
    );
};
```

---

## Dialog Component Pattern

### Standard Dialog Structure

All dialogs should have:
- Title with optional icon
- Close button (X)
- Action buttons at bottom

```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Info } from "lucide-react";

interface MyDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onConfirm: () => void;
}

export const MyDialog: React.FC<MyDialogProps> = ({ open, onOpenChange, onConfirm }) => {
    const handleConfirm = () => {
        onConfirm();
        onOpenChange(false);
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <Info className="h-5 w-5 text-primary" />
                        Confirmation Dialog
                    </DialogTitle>
                    <DialogDescription>
                        Are you sure you want to proceed with this action?
                    </DialogDescription>
                </DialogHeader>

                <div className="py-4">
                    {/* Dialog content */}
                    <p className="text-sm text-muted-foreground">
                        This action cannot be undone.
                    </p>
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={() => onOpenChange(false)}>
                        Cancel
                    </Button>
                    <Button onClick={handleConfirm}>
                        Confirm
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
};

// Usage
export const ParentComponent: React.FC = () => {
    const [dialogOpen, setDialogOpen] = useState(false);

    const handleConfirm = () => {
        console.log('Confirmed!');
    };

    return (
        <>
            <Button onClick={() => setDialogOpen(true)}>
                Open Dialog
            </Button>

            <MyDialog
                open={dialogOpen}
                onOpenChange={setDialogOpen}
                onConfirm={handleConfirm}
            />
        </>
    );
};
```

### Alert Dialog for Destructive Actions

```typescript
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { AlertTriangle } from "lucide-react";

interface DeleteDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onConfirm: () => void;
    itemName: string;
}

export const DeleteDialog: React.FC<DeleteDialogProps> = ({
    open,
    onOpenChange,
    onConfirm,
    itemName,
}) => {
    return (
        <AlertDialog open={open} onOpenChange={onOpenChange}>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle className="flex items-center gap-2">
                        <AlertTriangle className="h-5 w-5 text-destructive" />
                        Delete {itemName}
                    </AlertDialogTitle>
                    <AlertDialogDescription>
                        This action cannot be undone. This will permanently delete
                        the {itemName} from our servers.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction
                        onClick={onConfirm}
                        className="bg-destructive hover:bg-destructive/90"
                    >
                        Delete
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    );
};
```

---

## Table Pattern (Data Display)

### shadcn Table Component

shadcn uses Table components instead of DataGrid. For complex data grids, you can integrate TanStack Table.

```typescript
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useSuspenseQuery } from '@tanstack/react-query';

interface User {
    id: number;
    name: string;
    email: string;
    status: 'active' | 'inactive';
}

export const UsersTable: React.FC = () => {
    const { data: users } = useSuspenseQuery({
        queryKey: ['users'],
        queryFn: () => api.getUsers(),
    });

    return (
        <div className="rounded-md border">
            <Table>
                <TableCaption>A list of all users in the system.</TableCaption>
                <TableHeader>
                    <TableRow className="bg-muted/50">
                        <TableHead className="font-semibold">Name</TableHead>
                        <TableHead className="font-semibold">Email</TableHead>
                        <TableHead className="font-semibold">Status</TableHead>
                        <TableHead className="text-right font-semibold">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {users.map((user: User) => (
                        <TableRow
                            key={user.id}
                            className="hover:bg-muted/50 transition-colors"
                        >
                            <TableCell className="font-medium">{user.name}</TableCell>
                            <TableCell>{user.email}</TableCell>
                            <TableCell>
                                <Badge variant={user.status === 'active' ? 'default' : 'secondary'}>
                                    {user.status}
                                </Badge>
                            </TableCell>
                            <TableCell className="text-right">
                                <Button variant="ghost" size="sm">
                                    Edit
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </div>
    );
};
```

### TanStack Table Integration (Advanced)

For sorting, filtering, and pagination:

```typescript
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  ColumnDef,
  flexRender,
} from '@tanstack/react-table';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from 'react';

interface User {
    id: number;
    name: string;
    email: string;
}

const columns: ColumnDef<User>[] = [
    {
        accessorKey: 'name',
        header: 'Name',
    },
    {
        accessorKey: 'email',
        header: 'Email',
    },
    {
        id: 'actions',
        cell: ({ row }) => (
            <Button variant="ghost" size="sm">
                Edit
            </Button>
        ),
    },
];

export const DataTable: React.FC<{ data: User[] }> = ({ data }) => {
    const [globalFilter, setGlobalFilter] = useState('');

    const table = useReactTable({
        data,
        columns,
        getCoreRowModel: getCoreRowModel(),
        getSortedRowModel: getSortedRowModel(),
        getFilteredRowModel: getFilteredRowModel(),
        getPaginationRowModel: getPaginationRowModel(),
        state: {
            globalFilter,
        },
        onGlobalFilterChange: setGlobalFilter,
    });

    return (
        <div className="space-y-4">
            <Input
                placeholder="Search..."
                value={globalFilter}
                onChange={(e) => setGlobalFilter(e.target.value)}
                className="max-w-sm"
            />

            <div className="rounded-md border">
                <Table>
                    <TableHeader>
                        {table.getHeaderGroups().map((headerGroup) => (
                            <TableRow key={headerGroup.id}>
                                {headerGroup.headers.map((header) => (
                                    <TableHead key={header.id}>
                                        {flexRender(
                                            header.column.columnDef.header,
                                            header.getContext()
                                        )}
                                    </TableHead>
                                ))}
                            </TableRow>
                        ))}
                    </TableHeader>
                    <TableBody>
                        {table.getRowModel().rows.map((row) => (
                            <TableRow key={row.id}>
                                {row.getVisibleCells().map((cell) => (
                                    <TableCell key={cell.id}>
                                        {flexRender(
                                            cell.column.columnDef.cell,
                                            cell.getContext()
                                        )}
                                    </TableCell>
                                ))}
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">
                    {table.getFilteredRowModel().rows.length} row(s)
                </div>
                <div className="flex items-center gap-2">
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => table.previousPage()}
                        disabled={!table.getCanPreviousPage()}
                    >
                        Previous
                    </Button>
                    <Button
                        variant="outline"
                        size="sm"
                        onClick={() => table.nextPage()}
                        disabled={!table.getCanNextPage()}
                    >
                        Next
                    </Button>
                </div>
            </div>
        </div>
    );
};
```

---

## Mutation Patterns

### Update with Cache Invalidation

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useToast } from "@/hooks/use-toast";

export const useUpdateEntity = () => {
    const queryClient = useQueryClient();
    const { toast } = useToast();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: any }) =>
            api.updateEntity(id, data),

        onSuccess: (result, variables) => {
            // Invalidate affected queries
            queryClient.invalidateQueries({ queryKey: ['entity', variables.id] });
            queryClient.invalidateQueries({ queryKey: ['entities'] });

            toast({
                title: "Success",
                description: "Entity updated successfully",
            });
        },

        onError: () => {
            toast({
                title: "Error",
                description: "Failed to update entity",
                variant: "destructive",
            });
        },
    });
};

// Usage
const updateEntity = useUpdateEntity();

const handleSave = () => {
    updateEntity.mutate({ id: 123, data: { name: 'New Name' } });
};
```

### Optimistic Updates

```typescript
export const useOptimisticUpdate = () => {
    const queryClient = useQueryClient();
    const { toast } = useToast();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<Entity> }) =>
            api.updateEntity(id, data),

        onMutate: async ({ id, data }) => {
            // Cancel outgoing refetches
            await queryClient.cancelQueries({ queryKey: ['entity', id] });

            // Snapshot previous value
            const previousEntity = queryClient.getQueryData(['entity', id]);

            // Optimistically update
            queryClient.setQueryData(['entity', id], (old: Entity) => ({
                ...old,
                ...data,
            }));

            return { previousEntity };
        },

        onError: (err, variables, context) => {
            // Rollback on error
            queryClient.setQueryData(
                ['entity', variables.id],
                context?.previousEntity
            );

            toast({
                title: "Error",
                description: "Failed to update. Changes reverted.",
                variant: "destructive",
            });
        },

        onSettled: (data, error, variables) => {
            // Refetch after mutation
            queryClient.invalidateQueries({ queryKey: ['entity', variables.id] });
        },
    });
};
```

---

## Toast Notifications

### Basic Toast Usage

```typescript
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";

export const MyComponent: React.FC = () => {
    const { toast } = useToast();

    const showSuccess = () => {
        toast({
            title: "Success",
            description: "Your changes have been saved.",
        });
    };

    const showError = () => {
        toast({
            title: "Error",
            description: "Something went wrong. Please try again.",
            variant: "destructive",
        });
    };

    const showWarning = () => {
        toast({
            title: "Warning",
            description: "This action requires confirmation.",
            variant: "default",
        });
    };

    return (
        <div className="flex gap-2">
            <Button onClick={showSuccess}>Success Toast</Button>
            <Button onClick={showError} variant="destructive">Error Toast</Button>
            <Button onClick={showWarning} variant="outline">Warning Toast</Button>
        </div>
    );
};
```

---

## State Management Patterns

### TanStack Query for Server State (PRIMARY)

Use TanStack Query for **all server data**:
- Fetching: useSuspenseQuery
- Mutations: useMutation
- Caching: Automatic
- Synchronization: Built-in

```typescript
// ✅ CORRECT - TanStack Query for server data
const { data: users } = useSuspenseQuery({
    queryKey: ['users'],
    queryFn: () => userApi.getUsers(),
});
```

### useState for UI State

Use `useState` for **local UI state only**:
- Form inputs (uncontrolled)
- Modal open/closed
- Selected tab
- Temporary UI flags

```typescript
// ✅ CORRECT - useState for UI state
const [modalOpen, setModalOpen] = useState(false);
const [selectedTab, setSelectedTab] = useState(0);
```

### Zustand for Global Client State (Minimal)

Use Zustand only for **global client state**:
- Theme preference
- Sidebar collapsed state
- User preferences (not from server)

```typescript
import { create } from 'zustand';

interface AppState {
    sidebarOpen: boolean;
    toggleSidebar: () => void;
}

export const useAppState = create<AppState>((set) => ({
    sidebarOpen: true,
    toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
```

**Avoid prop drilling** - use context or Zustand instead.

---

## Summary

**Common Patterns:**
- ✅ useAuth hook for current user (id, email, roles, username)
- ✅ React Hook Form + Zod for forms
- ✅ shadcn Form components for structured forms
- ✅ Dialog with optional icon + description
- ✅ AlertDialog for destructive actions
- ✅ shadcn Table for data display
- ✅ TanStack Table for advanced features
- ✅ Mutations with cache invalidation
- ✅ Optimistic updates for better UX
- ✅ Toast notifications for feedback
- ✅ TanStack Query for server state
- ✅ useState for UI state
- ✅ Zustand for global client state (minimal)

**See Also:**
- [data-fetching.md](data-fetching.md) - TanStack Query patterns
- [component-patterns.md](component-patterns.md) - Component structure
- [loading-and-error-states.md](loading-and-error-states.md) - Error handling
- [shadcn-components.md](shadcn-components.md) - Complete shadcn component catalog
