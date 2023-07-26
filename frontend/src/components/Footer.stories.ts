import type { Meta, StoryObj } from '@storybook/svelte';
import Footer from "./Footer.svelte";

const meta = {
  title: 'Component/Footer',
  component: Footer,
  tags: ['autodocs'],
} satisfies Meta<Footer>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {};