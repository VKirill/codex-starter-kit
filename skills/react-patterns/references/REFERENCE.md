# React Patterns Reference

> Source: Context7 — /websites/react_dev (React official documentation)
> Updated: 2026-03-11

## Performance Hooks

### useMemo — Cache Expensive Calculations

`useMemo` lets you cache the result of an expensive calculation between re-renders. It only re-computes when its dependencies change.

```js
import { useMemo } from 'react';

function ProductPage({ productId, referrer }) {
  const product = useData('/product/' + productId);

  const requirements = useMemo(() => {
    return computeRequirements(product);
  }, [product]);

  return <ShippingForm requirements={requirements} />;
}
```

### useCallback — Cache Function References

`useCallback` lets you cache a function definition between re-renders. Prevents child components from re-rendering when the function reference hasn't actually changed.

```js
import { useCallback } from 'react';

function ProductPage({ productId, referrer }) {
  const handleSubmit = useCallback((orderDetails) => {
    post('/product/' + productId + '/buy', {
      referrer,
      orderDetails,
    });
  }, [productId, referrer]);

  return <ShippingForm onSubmit={handleSubmit} />;
}
```

### Combined useMemo + useCallback

```js
import { useMemo, useCallback } from 'react';

function ProductPage({ productId, referrer }) {
  const product = useData('/product/' + productId);

  const requirements = useMemo(() => {
    return computeRequirements(product);
  }, [product]);

  const handleSubmit = useCallback((orderDetails) => {
    post('/product/' + productId + '/buy', {
      referrer,
      orderDetails,
    });
  }, [productId, referrer]);

  return (
    <div>
      <ShippingForm requirements={requirements} onSubmit={handleSubmit} />
    </div>
  );
}
```

**Key difference**: `useMemo` calls your function and caches its *result*. `useCallback` caches the *function itself*.

## Context API

### useContext — Consume Context

```js
import { useContext, createContext } from 'react';

const ThemeContext = createContext('light');

function MyComponent() {
  const theme = useContext(ThemeContext);
  return <div className={theme}>...</div>;
}
```

### Optimizing Context Values

When providing context values, wrap them in `useMemo` to prevent unnecessary re-renders of consumers.

```javascript
import { useCallback, useMemo } from 'react';

function MyApp() {
  const [currentUser, setCurrentUser] = useState(null);

  const login = useCallback((response) => {
    storeCredentials(response.credentials);
    setCurrentUser(response.user);
  }, []);

  const contextValue = useMemo(() => ({
    currentUser,
    login
  }), [currentUser, login]);

  return (
    <AuthContext value={contextValue}>
      <Page />
    </AuthContext>
  );
}
```

### Context + useReducer Pattern (Scaling Up)

Combine `useReducer` with Context for complex state management that scales across many components.

#### 1. Create contexts

```js
import { createContext } from 'react';

export const TasksContext = createContext(null);
export const TasksDispatchContext = createContext(null);
```

#### 2. Provide state and dispatch

```js
import { useReducer } from 'react';

function TasksProvider({ children }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);

  return (
    <TasksContext value={tasks}>
      <TasksDispatchContext value={dispatch}>
        {children}
      </TasksDispatchContext>
    </TasksContext>
  );
}
```

#### 3. Custom hooks for access

```js
export function useTasks() {
  return useContext(TasksContext);
}

export function useTasksDispatch() {
  return useContext(TasksDispatchContext);
}
```

#### 4. Use in components

```js
function TaskList() {
  const tasks = useTasks();
  const dispatch = useTasksDispatch();

  return (
    <ul>
      {tasks.map(task => (
        <li key={task.id}>
          {task.text}
          <button onClick={() => dispatch({ type: 'deleted', id: task.id })}>
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
```

## Custom Hooks

Custom hooks extract reusable logic from components. They must start with `use` and can call other hooks.

### Pattern: Data Fetching Hook

```js
function useData(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);

    fetch(url)
      .then(res => res.json())
      .then(data => {
        if (!cancelled) {
          setData(data);
          setLoading(false);
        }
      })
      .catch(err => {
        if (!cancelled) {
          setError(err);
          setLoading(false);
        }
      });

    return () => { cancelled = true; };
  }, [url]);

  return { data, loading, error };
}
```

### Pattern: Local Storage Hook

```js
function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}
```

## Hooks Reference

### State Hooks

| Hook | Purpose |
|------|---------|
| `useState` | Declare a state variable |
| `useReducer` | Declare state with reducer logic |

### Effect Hooks

| Hook | Purpose |
|------|---------|
| `useEffect` | Connect to external systems, run side effects |
| `useLayoutEffect` | Fire before browser repaint (measure layout) |
| `useInsertionEffect` | Fire before DOM mutations (CSS-in-JS) |

### Ref Hooks

| Hook | Purpose |
|------|---------|
| `useRef` | Declare a ref (mutable value that doesn't trigger re-render) |
| `useImperativeHandle` | Customize the ref exposed by a component |

### Context Hooks

| Hook | Purpose |
|------|---------|
| `useContext` | Read and subscribe to context |

### Performance Hooks

| Hook | Purpose |
|------|---------|
| `useMemo` | Cache a calculated value |
| `useCallback` | Cache a function definition |
| `useTransition` | Mark a state update as non-blocking |
| `useDeferredValue` | Defer updating a non-critical part of UI |

### Other Hooks

| Hook | Purpose |
|------|---------|
| `useId` | Generate unique IDs for accessibility |
| `useSyncExternalStore` | Subscribe to an external store |
| `useActionState` | Manage state of form actions |
| `useOptimistic` | Show optimistic state during async operations |

## Suspense

Suspense lets you display a fallback while child components are loading.

```jsx
import { Suspense } from 'react';

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Albums />
    </Suspense>
  );
}
```

### Nested Suspense Boundaries

```jsx
<Suspense fallback={<BigSpinner />}>
  <Biography />
  <Suspense fallback={<AlbumsGlimmer />}>
    <Panel>
      <Albums />
    </Panel>
  </Suspense>
</Suspense>
```

## Error Boundaries

Error boundaries catch JavaScript errors in their child component tree and display a fallback UI.

```jsx
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    logErrorToService(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }
    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<p>Something went wrong</p>}>
  <Profile />
</ErrorBoundary>
```

## memo — Skip Unnecessary Re-renders

```jsx
import { memo } from 'react';

const ShippingForm = memo(function ShippingForm({ requirements, onSubmit }) {
  // Only re-renders when requirements or onSubmit change
  return <form onSubmit={onSubmit}>...</form>;
});
```

**When to use memo:**
- Component renders often with the same props
- Component is expensive to render
- Props are stable (use `useMemo`/`useCallback` for objects/functions)

**When NOT to use memo:**
- Component always receives different props
- Component is cheap to render
- You're just wrapping everything "just in case"

## Portals

Portals render children into a DOM node outside the parent component hierarchy.

```jsx
import { createPortal } from 'react-dom';

function Modal({ children }) {
  return createPortal(
    <div className="modal">{children}</div>,
    document.getElementById('modal-root')
  );
}
```

## Refs

### DOM Refs

```jsx
import { useRef } from 'react';

function TextInput() {
  const inputRef = useRef(null);

  function handleClick() {
    inputRef.current.focus();
  }

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>Focus</button>
    </>
  );
}
```

### Forwarding Refs

```jsx
import { forwardRef } from 'react';

const MyInput = forwardRef(function MyInput(props, ref) {
  return <input {...props} ref={ref} />;
});

// Parent can now access the input DOM node
function Form() {
  const inputRef = useRef(null);
  return <MyInput ref={inputRef} />;
}
```

## Server Components (React 19+)

Server Components run only on the server and are never sent to the client. They can:
- Directly access databases, filesystems, and other server resources
- Reduce client bundle size (server-only code is not shipped)
- Use `async/await` at the component level

```jsx
// Server Component (default in App Router)
async function BlogPost({ id }) {
  const post = await db.posts.findById(id);
  return <article>{post.content}</article>;
}

// Client Component (must opt-in)
'use client';
function LikeButton({ postId }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>Like</button>;
}
```

## Concurrent Features

### useTransition

Mark state updates as non-urgent to keep the UI responsive.

```jsx
import { useTransition } from 'react';

function TabContainer() {
  const [isPending, startTransition] = useTransition();
  const [tab, setTab] = useState('about');

  function selectTab(nextTab) {
    startTransition(() => {
      setTab(nextTab);
    });
  }

  return (
    <>
      <TabButton onClick={() => selectTab('about')}>About</TabButton>
      <TabButton onClick={() => selectTab('posts')}>Posts</TabButton>
      {isPending ? <Spinner /> : <TabPanel tab={tab} />}
    </>
  );
}
```

### useDeferredValue

Defer updating a non-critical part of the UI.

```jsx
import { useDeferredValue } from 'react';

function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  const results = useMemo(() => filterResults(deferredQuery), [deferredQuery]);

  return (
    <ul style={{ opacity: query !== deferredQuery ? 0.5 : 1 }}>
      {results.map(item => <li key={item.id}>{item.name}</li>)}
    </ul>
  );
}
```

## Performance Optimization Checklist

1. **Avoid unnecessary state** — derive values from existing state/props when possible
2. **Lift state up sparingly** — only when sibling components need the same state
3. **Use keys properly** — stable, unique keys for list items
4. **Memoize expensive calculations** with `useMemo`
5. **Stabilize callbacks** with `useCallback` (when passing to memoized children)
6. **Wrap pure components** with `memo` (only when profiling shows benefit)
7. **Split context** — separate frequently changing values from stable ones
8. **Use `useTransition`** for non-urgent state updates
9. **Use `useDeferredValue`** for expensive derived rendering
10. **Lazy load components** with `React.lazy` + `Suspense`
