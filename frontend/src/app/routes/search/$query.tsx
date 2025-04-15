import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/search/$query')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/search/$query"!</div>
}
