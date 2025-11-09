# Complete Examples

Full working examples combining all modern patterns: React.FC, lazy loading, Suspense, useSuspenseQuery, shadcn/ui, Tailwind styling, routing, and error handling.

---

## Example 1: Complete Modern Component

Combines: React.FC, useSuspenseQuery, cache-first, useCallback, shadcn components, Tailwind styling

```typescript
/**
 * User profile display component
 * Demonstrates modern patterns with Suspense and TanStack Query
 */
import React, { useState, useCallback, useMemo } from 'react';
import { useSuspenseQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardHeader, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useToast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";
import { userApi } from '../api/userApi';
import type { User } from '~types/user';

interface UserProfileProps {
    userId: string;
    onUpdate?: () => void;
    className?: string;
}

export const UserProfile: React.FC<UserProfileProps> = ({
    userId,
    onUpdate,
    className
}) => {
    const queryClient = useQueryClient();
    const { toast } = useToast();
    const [isEditing, setIsEditing] = useState(false);

    // Suspense query - no isLoading needed!
    const { data: user } = useSuspenseQuery({
        queryKey: ['user', userId],
        queryFn: () => userApi.getUser(userId),
        staleTime: 5 * 60 * 1000,
    });

    // Update mutation
    const updateMutation = useMutation({
        mutationFn: (updates: Partial<User>) =>
            userApi.updateUser(userId, updates),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['user', userId] });
            toast({
                title: "Success",
                description: "Profile updated successfully",
            });
            setIsEditing(false);
            onUpdate?.();
        },

        onError: () => {
            toast({
                title: "Error",
                description: "Failed to update profile",
                variant: "destructive",
            });
        },
    });

    // Memoized computed value
    const fullName = useMemo(() => {
        return `${user.firstName} ${user.lastName}`;
    }, [user.firstName, user.lastName]);

    const initials = useMemo(() => {
        return `${user.firstName[0]}${user.lastName[0]}`;
    }, [user.firstName, user.lastName]);

    // Event handlers with useCallback
    const handleEdit = useCallback(() => {
        setIsEditing(true);
    }, []);

    const handleSave = useCallback(() => {
        updateMutation.mutate({
            firstName: user.firstName,
            lastName: user.lastName,
        });
    }, [user, updateMutation]);

    const handleCancel = useCallback(() => {
        setIsEditing(false);
    }, []);

    return (
        <Card className={cn("max-w-2xl mx-auto", className)}>
            <CardHeader>
                <div className="flex items-center gap-4">
                    <Avatar className="h-16 w-16">
                        <AvatarFallback className="text-lg">
                            {initials}
                        </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                        <h2 className="text-2xl font-semibold">{fullName}</h2>
                        <p className="text-sm text-muted-foreground">{user.email}</p>
                    </div>
                </div>
            </CardHeader>

            <CardContent className="space-y-4">
                <div className="space-y-2">
                    <p className="text-sm">
                        <span className="font-medium">Username:</span> {user.username}
                    </p>
                    <p className="text-sm">
                        <span className="font-medium">Roles:</span> {user.roles.join(', ')}
                    </p>
                </div>

                <div className="flex items-center gap-2">
                    {!isEditing ? (
                        <Button onClick={handleEdit}>
                            Edit Profile
                        </Button>
                    ) : (
                        <>
                            <Button
                                onClick={handleSave}
                                disabled={updateMutation.isPending}
                            >
                                {updateMutation.isPending ? 'Saving...' : 'Save'}
                            </Button>
                            <Button
                                variant="outline"
                                onClick={handleCancel}
                            >
                                Cancel
                            </Button>
                        </>
                    )}
                </div>
            </CardContent>
        </Card>
    );
};

export default UserProfile;
```

**Usage:**
```typescript
<Suspense fallback={<LoadingSpinner />}>
    <UserProfile userId='123' onUpdate={() => console.log('Updated')} />
</Suspense>
```

---

## Example 2: Complete Feature Structure

Real example based on `features/users/`:

```
features/
  users/
    api/
      userApi.ts                # API service layer
    components/
      UserProfile.tsx           # Main component (from Example 1)
      UserList.tsx              # List component
      UserCard.tsx              # Card component
      modals/
        DeleteUserModal.tsx     # Modal component
    hooks/
      useSuspenseUser.ts        # Suspense query hook
      useUserMutations.ts       # Mutation hooks
      useUserPermissions.ts     # Feature-specific hook
    helpers/
      userHelpers.ts            # Utility functions
      validation.ts             # Validation logic
    types/
      index.ts                  # TypeScript interfaces
    index.ts                    # Public API exports
```

### API Service (userApi.ts)

```typescript
import apiClient from '@/lib/apiClient';
import type { User, CreateUserPayload, UpdateUserPayload } from '../types';

export const userApi = {
    getUser: async (userId: string): Promise<User> => {
        const { data } = await apiClient.get(`/users/${userId}`);
        return data;
    },

    getUsers: async (): Promise<User[]> => {
        const { data } = await apiClient.get('/users');
        return data;
    },

    createUser: async (payload: CreateUserPayload): Promise<User> => {
        const { data } = await apiClient.post('/users', payload);
        return data;
    },

    updateUser: async (userId: string, payload: UpdateUserPayload): Promise<User> => {
        const { data } = await apiClient.put(`/users/${userId}`, payload);
        return data;
    },

    deleteUser: async (userId: string): Promise<void> => {
        await apiClient.delete(`/users/${userId}`);
    },
};
```

### Suspense Hook (useSuspenseUser.ts)

```typescript
import { useSuspenseQuery } from '@tanstack/react-query';
import { userApi } from '../api/userApi';
import type { User } from '../types';

export function useSuspenseUser(userId: string) {
    return useSuspenseQuery<User, Error>({
        queryKey: ['user', userId],
        queryFn: () => userApi.getUser(userId),
        staleTime: 5 * 60 * 1000,
        gcTime: 10 * 60 * 1000,
    });
}

export function useSuspenseUsers() {
    return useSuspenseQuery<User[], Error>({
        queryKey: ['users'],
        queryFn: () => userApi.getUsers(),
        staleTime: 1 * 60 * 1000,  // Shorter for list
    });
}
```

### Types (types/index.ts)

```typescript
export interface User {
    id: string;
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    roles: string[];
    createdAt: string;
    updatedAt: string;
}

export interface CreateUserPayload {
    username: string;
    email: string;
    firstName: string;
    lastName: string;
    password: string;
}

export type UpdateUserPayload = Partial<Omit<User, 'id' | 'createdAt' | 'updatedAt'>>;
```

### Public Exports (index.ts)

```typescript
// Export components
export { UserProfile } from './components/UserProfile';
export { UserList } from './components/UserList';

// Export hooks
export { useSuspenseUser, useSuspenseUsers } from './hooks/useSuspenseUser';
export { useUserMutations } from './hooks/useUserMutations';

// Export API
export { userApi } from './api/userApi';

// Export types
export type { User, CreateUserPayload, UpdateUserPayload } from './types';
```

---

## Example 3: Complete Route with Lazy Loading

```typescript
/**
 * User profile route
 * Path: /users/:userId
 */

import { createFileRoute } from '@tanstack/react-router';
import { lazy, Suspense } from 'react';
import { LoadingSpinner } from '~components/LoadingSpinner';

// Lazy load the UserProfile component
const UserProfile = lazy(() =>
    import('@/features/users/components/UserProfile').then(
        (module) => ({ default: module.UserProfile })
    )
);

export const Route = createFileRoute('/users/$userId')({
    component: UserProfilePage,
    loader: ({ params }) => ({
        crumb: `User ${params.userId}`,
    }),
});

function UserProfilePage() {
    const { userId } = Route.useParams();

    return (
        <div className="container py-6">
            <Suspense fallback={<LoadingSpinner />}>
                <UserProfile
                    userId={userId}
                    onUpdate={() => console.log('Profile updated')}
                />
            </Suspense>
        </div>
    );
}

export default UserProfilePage;
```

---

## Example 4: List with Search and Filtering

```typescript
import React, { useState, useMemo } from 'react';
import { useSuspenseQuery } from '@tanstack/react-query';
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useDebounce } from 'use-debounce';
import { userApi } from '../api/userApi';

export const UserList: React.FC = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [debouncedSearch] = useDebounce(searchTerm, 300);

    const { data: users } = useSuspenseQuery({
        queryKey: ['users'],
        queryFn: () => userApi.getUsers(),
    });

    // Memoized filtering
    const filteredUsers = useMemo(() => {
        if (!debouncedSearch) return users;

        return users.filter(user =>
            user.name.toLowerCase().includes(debouncedSearch.toLowerCase()) ||
            user.email.toLowerCase().includes(debouncedSearch.toLowerCase())
        );
    }, [users, debouncedSearch]);

    return (
        <div className="space-y-4">
            <Input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search users..."
                className="max-w-md"
            />

            <div className="space-y-2">
                {filteredUsers.map(user => (
                    <Card key={user.id} className="p-4 hover:bg-muted/50 transition-colors">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="font-medium">{user.name}</p>
                                <p className="text-sm text-muted-foreground">{user.email}</p>
                            </div>
                            {user.active && (
                                <Badge>Active</Badge>
                            )}
                        </div>
                    </Card>
                ))}
            </div>

            {filteredUsers.length === 0 && (
                <p className="text-center text-muted-foreground py-8">
                    No users found
                </p>
            )}
        </div>
    );
};
```

---

## Example 5: Form with Validation

```typescript
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Card, CardHeader, CardContent, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";
import { userApi } from '../api/userApi';

const userSchema = z.object({
    username: z.string().min(3).max(50),
    email: z.string().email(),
    firstName: z.string().min(1),
    lastName: z.string().min(1),
});

type UserFormData = z.infer<typeof userSchema>;

interface CreateUserFormProps {
    onSuccess?: () => void;
}

export const CreateUserForm: React.FC<CreateUserFormProps> = ({ onSuccess }) => {
    const queryClient = useQueryClient();
    const { toast } = useToast();

    const form = useForm<UserFormData>({
        resolver: zodResolver(userSchema),
        defaultValues: {
            username: '',
            email: '',
            firstName: '',
            lastName: '',
        },
    });

    const createMutation = useMutation({
        mutationFn: (data: UserFormData) => userApi.createUser(data),

        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
            toast({
                title: "Success",
                description: "User created successfully",
            });
            form.reset();
            onSuccess?.();
        },

        onError: () => {
            toast({
                title: "Error",
                description: "Failed to create user",
                variant: "destructive",
            });
        },
    });

    const onSubmit = (data: UserFormData) => {
        createMutation.mutate(data);
    };

    return (
        <Card className="max-w-lg">
            <CardHeader>
                <CardTitle>Create New User</CardTitle>
            </CardHeader>
            <CardContent>
                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                        <FormField
                            control={form.control}
                            name="username"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Username</FormLabel>
                                    <FormControl>
                                        <Input placeholder="johndoe" {...field} />
                                    </FormControl>
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
                                        <Input type="email" placeholder="john@example.com" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="firstName"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>First Name</FormLabel>
                                    <FormControl>
                                        <Input placeholder="John" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <FormField
                            control={form.control}
                            name="lastName"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Last Name</FormLabel>
                                    <FormControl>
                                        <Input placeholder="Doe" {...field} />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <Button
                            type="submit"
                            className="w-full"
                            disabled={createMutation.isPending}
                        >
                            {createMutation.isPending ? 'Creating...' : 'Create User'}
                        </Button>
                    </form>
                </Form>
            </CardContent>
        </Card>
    );
};

export default CreateUserForm;
```

---

## Example 6: Parent Container with Lazy Loading

```typescript
import React, { Suspense } from 'react';
import { LoadingSpinner } from '~components/LoadingSpinner';

// Lazy load heavy components
const UserList = React.lazy(() => import('./UserList'));
const UserStats = React.lazy(() => import('./UserStats'));
const ActivityFeed = React.lazy(() => import('./ActivityFeed'));

export const UserDashboard: React.FC = () => {
    return (
        <div className="p-6 space-y-6">
            <Suspense fallback={<LoadingSpinner />}>
                <UserStats />
            </Suspense>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                    <Suspense fallback={<LoadingSpinner />}>
                        <UserList />
                    </Suspense>
                </div>

                <div className="lg:col-span-1">
                    <Suspense fallback={<LoadingSpinner />}>
                        <ActivityFeed />
                    </Suspense>
                </div>
            </div>
        </div>
    );
};

export default UserDashboard;
```

**Benefits:**
- Each section loads independently
- User sees partial content sooner
- Better perceived performance
- Uses Tailwind grid for responsive layout

---

## Example 7: Cache-First Strategy Implementation

Complete example based on smart caching patterns:

```typescript
import { useSuspenseQuery, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../api/postApi';
import type { Post } from '../types';

/**
 * Smart post hook with cache-first strategy
 * Reuses data from grid cache when available
 */
export function useSuspensePost(projectId: number, postId: number) {
    const queryClient = useQueryClient();

    return useSuspenseQuery<Post, Error>({
        queryKey: ['post', projectId, postId],
        queryFn: async () => {
            // Strategy 1: Check grid cache first (avoids API call)
            const gridCache = queryClient.getQueryData<{ rows: Post[] }>([
                'posts-v2',
                projectId,
                'summary'
            ]) || queryClient.getQueryData<{ rows: Post[] }>([
                'posts-v2',
                projectId,
                'flat'
            ]);

            if (gridCache?.rows) {
                const cached = gridCache.rows.find(
                    (row) => row.id === postId
                );

                if (cached) {
                    return cached;  // Return from cache - no API call!
                }
            }

            // Strategy 2: Not in cache, fetch from API
            return postApi.getPost(projectId, postId);
        },
        staleTime: 5 * 60 * 1000,       // Fresh for 5 minutes
        gcTime: 10 * 60 * 1000,          // Cache for 10 minutes
        refetchOnWindowFocus: false,     // Don't refetch on focus
    });
}
```

**Why this pattern:**
- Checks grid cache before API
- Instant data if user came from grid
- Falls back to API if not cached
- Configurable cache times

---

## Example 8: Dialog with Form

```typescript
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { UserPlus } from "lucide-react";

const formSchema = z.object({
    name: z.string().min(1, "Name is required"),
    email: z.string().email("Invalid email"),
});

type FormData = z.infer<typeof formSchema>;

interface AddUserDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onSubmit: (data: FormData) => Promise<void>;
}

export const AddUserDialog: React.FC<AddUserDialogProps> = ({
    open,
    onOpenChange,
    onSubmit,
}) => {
    const { register, handleSubmit, formState: { errors }, reset } = useForm<FormData>({
        resolver: zodResolver(formSchema),
    });

    const handleClose = () => {
        reset();
        onOpenChange(false);
    };

    const handleFormSubmit = async (data: FormData) => {
        await onSubmit(data);
        handleClose();
    };

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <UserPlus className="h-5 w-5 text-primary" />
                        Add User
                    </DialogTitle>
                    <DialogDescription>
                        Create a new user account. Fill in the details below.
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit(handleFormSubmit)}>
                    <div className="space-y-4 py-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">Name</Label>
                            <Input
                                id="name"
                                autoFocus
                                {...register('name')}
                                className={errors.name ? 'border-destructive' : ''}
                            />
                            {errors.name && (
                                <p className="text-sm text-destructive">{errors.name.message}</p>
                            )}
                        </div>

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
                    </div>

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={handleClose}>
                            Cancel
                        </Button>
                        <Button type="submit">
                            Add User
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
};
```

---

## Example 9: Parallel Data Fetching

```typescript
import React from 'react';
import { useSuspenseQueries } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { userApi } from '../api/userApi';
import { statsApi } from '../api/statsApi';
import { activityApi } from '../api/activityApi';

export const Dashboard: React.FC = () => {
    // Fetch all data in parallel with Suspense
    const [statsQuery, usersQuery, activityQuery] = useSuspenseQueries({
        queries: [
            {
                queryKey: ['stats'],
                queryFn: () => statsApi.getStats(),
            },
            {
                queryKey: ['users', 'active'],
                queryFn: () => userApi.getActiveUsers(),
            },
            {
                queryKey: ['activity', 'recent'],
                queryFn: () => activityApi.getRecent(),
            },
        ],
    });

    return (
        <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Stats</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">{statsQuery.data.total}</p>
                        <p className="text-sm text-muted-foreground">Total Items</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Active Users</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">{usersQuery.data.length}</p>
                        <p className="text-sm text-muted-foreground">Currently Active</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">{activityQuery.data.length}</p>
                        <p className="text-sm text-muted-foreground">Events Today</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};

// Usage with Suspense
<Suspense fallback={<LoadingSpinner />}>
    <Dashboard />
</Suspense>
```

---

## Example 10: Optimistic Update

```typescript
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useToast } from "@/hooks/use-toast";
import type { User } from '../types';

export const useToggleUserStatus = () => {
    const queryClient = useQueryClient();
    const { toast } = useToast();

    return useMutation({
        mutationFn: (userId: string) => userApi.toggleStatus(userId),

        // Optimistic update
        onMutate: async (userId) => {
            // Cancel outgoing refetches
            await queryClient.cancelQueries({ queryKey: ['users'] });

            // Snapshot previous value
            const previousUsers = queryClient.getQueryData<User[]>(['users']);

            // Optimistically update UI
            queryClient.setQueryData<User[]>(['users'], (old) => {
                return old?.map(user =>
                    user.id === userId
                        ? { ...user, active: !user.active }
                        : user
                ) || [];
            });

            return { previousUsers };
        },

        // Rollback on error
        onError: (err, userId, context) => {
            queryClient.setQueryData(['users'], context?.previousUsers);
            toast({
                title: "Error",
                description: "Failed to update status. Changes reverted.",
                variant: "destructive",
            });
        },

        // Refetch after mutation
        onSettled: () => {
            queryClient.invalidateQueries({ queryKey: ['users'] });
        },

        onSuccess: () => {
            toast({
                title: "Success",
                description: "User status updated",
            });
        },
    });
};
```

---

## Summary

**Key Takeaways:**

1. **Component Pattern**: React.FC + lazy + Suspense + useSuspenseQuery
2. **Feature Structure**: Organized subdirectories (api/, components/, hooks/, etc.)
3. **Routing**: File-based with lazy loading
4. **Data Fetching**: useSuspenseQuery with cache-first strategy
5. **Forms**: React Hook Form + Zod validation + shadcn Form components
6. **Error Handling**: useToast + onError callbacks
7. **Performance**: useMemo, useCallback, React.memo, debouncing
8. **Styling**: shadcn/ui components + Tailwind CSS classes
9. **Dialogs**: shadcn Dialog components with form integration
10. **Mutations**: Optimistic updates for better UX

**See other resources for detailed explanations of each pattern.**
