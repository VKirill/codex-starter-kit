<!-- Source: https://wagmi.sh/llms-full.txt (llms-full.txt) -->
<!-- Downloaded: 2026-03-21 -->

---
url: /tempo/actions/amm.burn.md
---
# `amm.burn`

Burns liquidity tokens and receives the underlying token pair. [Learn more about the Fee AMM](https://docs.tempo.xyz/protocol/fees/spec-fee-amm)

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.burn.md","from":213,"to":8601}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"15a04714fe58dc0283f87db9029cec245122d1b5c43e71becacad49ab6778a83","data":"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="}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const { amountUserToken, amountValidatorToken, receipt } =
  await Actions.amm.burnSync(config, {
    liquidity: parseUnits('10.5', 18),
    to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
    userToken: '0x20c0000000000000000000000000000000000000',
    validatorToken: '0x20c0000000000000000000000000000000000001',
  })

console.log('Received user tokens:', amountUserToken)
// @log: Received user tokens: 5250000000000000000n
console.log('Received validator tokens:', amountValidatorToken)
// @log: Received validator tokens: 5250000000000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `amm.burn` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.burn.md","from":8937,"to":9561}<fsm-4or7z6pudsq>
import { Actions as viem_Actions } from 'viem/tempo'
import { Actions } from 'wagmi/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'

const hash = await Actions.amm.burn(config, {
  liquidity: parseUnits('10.5', 18),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { amountUserToken, amountValidatorToken } }
  = viem_Actions.amm.burn.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.burn.md","from":9588,"to":10122}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Amount of user tokens received */
  amountUserToken: bigint
  /** Amount of validator tokens received */
  amountValidatorToken: bigint
  /** Amount of liquidity tokens burned */
  liquidity: bigint
  /** Transaction receipt */
  receipt: TransactionReceipt
  /** Address that initiated the burn */
  sender: Address
  /** Address that received the underlying tokens */
  to: Address
  /** Address of the user token */
  userToken: Address
  /** Address of the validator token */
  validatorToken: Address
}
```

## Parameters

### liquidity

* **Type:** `bigint`

Amount of LP tokens to burn.

### to

* **Type:** `Address`

Address to send tokens to.

### userToken

* **Type:** `Address | bigint`

Address or ID of the user token.

### validatorToken

* **Type:** `Address | bigint`

Address or ID of the validator token.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`amm.burn`](https://viem.sh/tempo/actions/amm.burn)

---

---
url: /tempo/actions/amm.getLiquidityBalance.md
---
# `amm.getLiquidityBalance`

Gets the liquidity balance for an address in a specific pool.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.getLiquidityBalance.md","from":145,"to":5397}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"685594825d16d8c180f2d81984cf6bf8e0a654c6d4ca8ae78262e8340a1d1fb4","data":"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="}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const balance = await Actions.amm.getLiquidityBalance(config, {
  address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('Liquidity balance:', balance)
// @log: Liquidity balance: 10500000000000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

`bigint`

Liquidity balance.

## Parameters

### address

* **Type:** `Address`

Address to check balance for.

### poolId (optional)

* **Type:** `Hex`

Pool ID.

### userToken (optional)

* **Type:** `Address | bigint`

User token.

### validatorToken (optional)

* **Type:** `Address | bigint`

Validator token.

## Viem

* [`amm.getLiquidityBalance`](https://viem.sh/tempo/actions/amm.getLiquidityBalance)

---

---
url: /tempo/actions/amm.getPool.md
---
# `amm.getPool`

Gets the reserves for a liquidity pool.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.getPool.md","from":112,"to":9506}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"7dda7bb1ad17e8af2b2215af2a34e1eccb912d3acf16ffbd8338a2da0631fe20","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const pool = await Actions.amm.getPool(config, {
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('User token reserve:', pool.reserveUserToken)
// @log: User token reserve: 1000000000000000000000n
console.log('Validator token reserve:', pool.reserveValidatorToken)
// @log: Validator token reserve: 1000000000000000000000n
console.log('Total supply:', pool.totalSupply)
// @log: Total supply: 1000000000000000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.getPool.md","from":9592,"to":9797}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Reserve of user token */
  reserveUserToken: bigint
  /** Reserve of validator token */
  reserveValidatorToken: bigint
  /** Total supply of LP tokens */
  totalSupply: bigint
}
```

## Parameters

### userToken

* **Type:** `Address | bigint`

Address or ID of the user token.

### validatorToken

* **Type:** `Address | bigint`

Address or ID of the validator token.

## Viem

* [`amm.getPool`](https://viem.sh/tempo/actions/amm.getPool)

---

---
url: /tempo/actions/amm.mint.md
---
# `amm.mint`

Mints liquidity tokens by providing a token pair. [Learn more about the Fee AMM](https://docs.tempo.xyz/protocol/fees/spec-fee-amm)

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.mint.md","from":201,"to":6391}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"8c8d9e3a10d7fc7ac97a66b8da388430eb2e46abfa5de1aeb9fd7c017dfd2448","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const { liquidity, receipt } = await Actions.amm.mintSync(config, {
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userTokenAddress: '0x20c0000000000000000000000000000000000000',
  validatorTokenAddress: '0x20c0000000000000000000000000000000000001',
  validatorTokenAmount: parseUnits('100', 6),
})

console.log('Liquidity minted:', liquidity)
// @log: Liquidity minted: 100000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `amm.mint` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.mint.md","from":6729,"to":7348}<fsm-4or7z6pudsq>
import { Actions as viem_Actions } from 'viem/tempo'
import { Actions } from 'wagmi/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'

const hash = await Actions.amm.mint(config, {
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userTokenAddress: '0x20c0000000000000000000000000000000000000',
  validatorTokenAddress: '0x20c0000000000000000000000000000000000001',
  validatorTokenAmount: parseUnits('100', 6),
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { liquidity } }
  = viem_Actions.amm.mint.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.mint.md","from":7375,"to":7842}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Amount of user tokens provided */
  amountUserToken: bigint
  /** Amount of validator tokens provided */
  amountValidatorToken: bigint
  /** Amount of liquidity tokens minted */
  liquidity: bigint
  /** Transaction receipt */
  receipt: TransactionReceipt
  /** Address that initiated the mint */
  sender: Address
  /** Address of the user token */
  userToken: Address
  /** Address of the validator token */
  validatorToken: Address
}
```

## Parameters

### to

* **Type:** `Address`

Address to mint the liquidity tokens to.

### userTokenAddress

* **Type:** `Address | bigint`

User token address.

### validatorTokenAddress

* **Type:** `Address | bigint`

Validator token address.

### validatorTokenAmount

* **Type:** `bigint`

Amount of validator tokens to provide.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`amm.mint`](https://viem.sh/tempo/actions/amm.mint)

---

---
url: /tempo/actions/amm.rebalanceSwap.md
---
# `amm.rebalanceSwap`

Performs a rebalance swap between user and validator tokens. [Learn more about the Fee AMM](https://docs.tempo.xyz/protocol/fees/spec-fee-amm)

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.rebalanceSwap.md","from":221,"to":6288}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"e399d67fb11f22f03c5401507bb51f3428c3c4c6a5e925ed4f4bc4e8e55c065a","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const { amountIn, receipt } = await Actions.amm.rebalanceSwapSync(config, {
  amountOut: parseUnits('10.5', 6),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('Amount in:', amountIn)
// @log: 10605000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `amm.rebalanceSwap` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.rebalanceSwap.md","from":6635,"to":7247}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { Actions as viem_Actions } from 'viem/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'

const hash = await Actions.amm.rebalanceSwap(config, {
  amountOut: parseUnits('10.5', 6),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { amountIn } }
  = viem_Actions.amm.rebalanceSwap.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.rebalanceSwap.md","from":7274,"to":7666}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Amount of tokens required for the swap */
  amountIn: bigint
  /** Amount of output tokens received */
  amountOut: bigint
  /** Transaction receipt */
  receipt: TransactionReceipt
  /** Address that initiated the swap */
  swapper: Address
  /** Address of the user token */
  userToken: Address
  /** Address of the validator token */
  validatorToken: Address
}
```

## Parameters

### amountOut

* **Type:** `bigint`

Amount of user token to receive.

### to

* **Type:** `Address`

Address to send the user token to.

### userToken

* **Type:** `Address | bigint`

Address or ID of the user token.

### validatorToken

* **Type:** `Address | bigint`

Address or ID of the validator token.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`amm.rebalanceSwap`](https://viem.sh/tempo/actions/amm.rebalanceSwap)

---

---
url: /tempo/hooks/amm.useBurn.md
---
# `amm.useBurn`

Burns liquidity tokens and receives the underlying token pair. [Learn more about the Fee AMM](https://docs.tempo.xyz/protocol/fees/spec-fee-amm)

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useBurn.md","from":216,"to":10037}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"f352a044790f8cbde9e59508d0e42c0dd85e637c21507c3fb59ad6574684cfad","data":"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="}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const burnSync = Hooks.amm.useBurnSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
burnSync.mutate({
  liquidity: parseUnits('10.5', 18),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('Received user tokens:', burnSync.data?.amountUserToken)
// @log: Received user tokens: 5250000000000000000n
console.log('Received validator tokens:', burnSync.data?.amountValidatorToken)
// @log: Received validator tokens: 5250000000000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `amm.burn` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useBurn.md","from":10373,"to":11081}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { parseUnits } from 'viem'
import { useWaitForTransactionReceipt } from 'wagmi'

const burn = Hooks.amm.useBurn()
const { data: receipt } = useWaitForTransactionReceipt({ hash: burn.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
burn.mutate({
  liquidity: parseUnits('10.5', 18),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

if (receipt) {
  const { args: { amountUserToken, amountValidatorToken } }
    = Actions.amm.burn.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `amm.burn` Return Type](/tempo/actions/amm.burn#return-type)

### mutate/mutateAsync

See [Wagmi Action `amm.burn` Parameters](/tempo/actions/amm.burn#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`amm.burn`](/tempo/actions/amm.burn)

---

---
url: /tempo/hooks/amm.useLiquidityBalance.md
---
# `amm.useLiquidityBalance`

Gets the liquidity balance for an address in a specific pool.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useLiquidityBalance.md","from":145,"to":5353}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"8ac7e459f30e286677d1cb839aa57883a14653c6b8b3bf03624ebf676bd6cacc","data":"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"}
import { Hooks } from 'wagmi/tempo'

const { data: balance } = Hooks.amm.useLiquidityBalance({
  address: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('Liquidity balance:', balance)
// @log: Liquidity balance: 10500000000000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `amm.getLiquidityBalance` Return Type](/tempo/actions/amm.getLiquidityBalance#return-type)

## Parameters

See [Wagmi Action `amm.getLiquidityBalance` Parameters](/tempo/actions/amm.getLiquidityBalance#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`amm.getLiquidityBalance`](/tempo/actions/amm.getLiquidityBalance)

---

---
url: /tempo/hooks/amm.useMint.md
---
# `amm.useMint`

Mints liquidity tokens by providing a token pair. [Learn more about the Fee AMM](https://docs.tempo.xyz/protocol/fees/spec-fee-amm)

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useMint.md","from":203,"to":7459}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"4fca6eaaab4d04b51aad961895f40c6a81566cafdac628c7923a2a2603d064ae","data":"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"}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const mintSync = Hooks.amm.useMintSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
mintSync.mutate({
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userTokenAddress: '0x20c0000000000000000000000000000000000000',
  validatorTokenAddress: '0x20c0000000000000000000000000000000000001',
  validatorTokenAmount: parseUnits('100', 6),
})

console.log('Liquidity minted:', mintSync.data?.liquidity)
// @log: Liquidity minted: 100000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `amm.mint` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useMint.md","from":7795,"to":8498}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { parseUnits } from 'viem'
import { useWaitForTransactionReceipt } from 'wagmi'

const mint = Hooks.amm.useMint()
const { data: receipt } = useWaitForTransactionReceipt({ hash: mint.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
mint.mutate({
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userTokenAddress: '0x20c0000000000000000000000000000000000000',
  validatorTokenAddress: '0x20c0000000000000000000000000000000000001',
  validatorTokenAmount: parseUnits('100', 6),
})

if (receipt) {
  const { args: { liquidity } }
    = Actions.amm.mint.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `amm.mint` Return Type](/tempo/actions/amm.mint#return-type)

### mutate/mutateAsync

See [Wagmi Action `amm.mint` Parameters](/tempo/actions/amm.mint#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`amm.mint`](/tempo/actions/amm.mint)

---

---
url: /tempo/hooks/amm.usePool.md
---
# `amm.usePool`

Gets the reserves for a liquidity pool.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.usePool.md","from":111,"to":9752}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"a5e2597c7cc0e903cdeee24bcbbc6a915a731be45436f6ef363478a4ecfdc54e","data":"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"}
import { Hooks } from 'wagmi/tempo'

const { data: pool } = Hooks.amm.usePool({
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('User token reserve:', pool?.reserveUserToken)
// @log: User token reserve: 1000000000000000000000n
console.log('Validator token reserve:', pool?.reserveValidatorToken)
// @log: Validator token reserve: 1000000000000000000000n
console.log('Total supply:', pool?.totalSupply)
// @log: Total supply: 1000000000000000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `amm.getPool` Return Type](/tempo/actions/amm.getPool#return-type)

## Parameters

See [Wagmi Action `amm.getPool` Parameters](/tempo/actions/amm.getPool#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`amm.getPool`](/tempo/actions/amm.getPool)

---

---
url: /tempo/hooks/amm.useRebalanceSwap.md
---
# `amm.useRebalanceSwap`

Performs a rebalance swap between user and validator tokens. [Learn more about the Fee AMM](https://docs.tempo.xyz/protocol/fees/spec-fee-amm)

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useRebalanceSwap.md","from":223,"to":7472}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"20c09f8cc1ff08a8faf46184bc97fb05274d872847ffff372666aabccf7c9bdd","data":"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"}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const rebalanceSwapSync = Hooks.amm.useRebalanceSwapSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
rebalanceSwapSync.mutate({
  amountOut: parseUnits('10.5', 6),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

console.log('Amount in:', rebalanceSwapSync.data?.amountIn)
// @log: 10605000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `amm.rebalanceSwap` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useRebalanceSwap.md","from":7817,"to":8540}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { parseUnits } from 'viem'
import { useWaitForTransactionReceipt } from 'wagmi'

const rebalanceSwap = Hooks.amm.useRebalanceSwap()
const { data: receipt } = useWaitForTransactionReceipt({ hash: rebalanceSwap.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
rebalanceSwap.mutate({
  amountOut: parseUnits('10.5', 6),
  to: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  userToken: '0x20c0000000000000000000000000000000000000',
  validatorToken: '0x20c0000000000000000000000000000000000001',
})

if (receipt) {
  const { args: { amountIn } }
    = Actions.amm.rebalanceSwap.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `amm.rebalanceSwap` Return Type](/tempo/actions/amm.rebalanceSwap#return-type)

### mutate/mutateAsync

See [Wagmi Action `amm.rebalanceSwap` Parameters](/tempo/actions/amm.rebalanceSwap#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`amm.rebalanceSwap`](/tempo/actions/amm.rebalanceSwap)

---

---
url: /tempo/hooks/amm.useWatchBurn.md
---
# `amm.useWatchBurn`

Watches for liquidity burn events on the Fee AMM.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useWatchBurn.md","from":128,"to":4832}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"1eb67ad9a75d59810fdaf0024451c348d0f712105fb6fc09eb9c9df760ca27f0","data":"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="}
import { Hooks } from 'wagmi/tempo'

Hooks.amm.useWatchBurn({
  onBurn: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `amm.watchBurn` Parameters](/tempo/actions/amm.watchBurn#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`amm.burn`](/tempo/actions/amm.burn)
* [`amm.watchBurn`](/tempo/actions/amm.watchBurn)

---

---
url: /tempo/hooks/amm.useWatchMint.md
---
# `amm.useWatchMint`

Watches for liquidity mint events on the Fee AMM.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useWatchMint.md","from":128,"to":4640}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"dcfbe669423c1e67e1fd5bfc996004b53912d26ef3dcef6280d135f90c3df485","data":"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"}
import { Hooks } from 'wagmi/tempo'

Hooks.amm.useWatchMint({
  onMint: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `amm.watchMint` Parameters](/tempo/actions/amm.watchMint#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`amm.mint`](/tempo/actions/amm.mint)
* [`amm.watchMint`](/tempo/actions/amm.watchMint)

---

---
url: /tempo/hooks/amm.useWatchRebalanceSwap.md
---
# `amm.useWatchRebalanceSwap`

Watches for rebalance swap events on the Fee AMM.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/amm.useWatchRebalanceSwap.md","from":137,"to":4883}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"a65363a61410810306bc28a64110f48e977141b2aff31cdee698fa19287f0ab5","data":"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"}
import { Hooks } from 'wagmi/tempo'

Hooks.amm.useWatchRebalanceSwap({
  onRebalanceSwap: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `amm.watchRebalanceSwap` Parameters](/tempo/actions/amm.watchRebalanceSwap#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`amm.rebalanceSwap`](/tempo/actions/amm.rebalanceSwap)
* [`amm.watchRebalanceSwap`](/tempo/actions/amm.watchRebalanceSwap)

---

---
url: /tempo/actions/amm.watchBurn.md
---
# `amm.watchBurn`

Watches for liquidity burn events on the Fee AMM.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchBurn.md","from":123,"to":5186}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"88643edeaab8a1c3858658b1397de9291730cd2a4ec09f2bcb6ee2f76ce6d305","data":"N4Igdg9gJgpgziAXAbVAFwJ4AcZJACwgDcYAnEAGhDRgA808BLAWywlLQAIBBAYzUYQwCKnDQBDDkgCcVADYwwAczT4kAdioTSSmA0Qg+AoSJBzGYXIgAMVXvknj+ZGQF8K6bFYLEXWuvogABTi5uJwAJScvCZcMWAAZoxKiJwAwkJJSgA6YCxsHNGZyZQgYpL6ACyaZooqaogAbFqSuoHxWaXmlkgAjHYOpE405IjS7p44eIQk5P70ePFinACuYADu4mj2qQDqW/YZYGhD/ACiJMcASnorpGAAKl6l5VKI6rK1yqoaLTp6eDWm22ankFisAGYBo5nKNGhNqM8DDM/NQAkxWOwuEZBMIXtp9AAOT4Kb4NGraNp4HEmLrgpBQkD2GEjPrwjyIqbI3xzNELAz5LGccTMZj4ioyGqk+oMv5UgwisVgnqIRnM06sxAAJkqCMwXJ8s1KNH5IASa34uM4wPsACE7mAADxHLIAPiCHWSqRdyQonCwjmYejIcFSNOEADpFRGbfh7fcIwAFQPB0hwZ3FJSuiJ7A74I4nYYXRRoG5oB1PHC5MAi+AB3gwa15+NgUpQCC8BAGfYg+CcBLsTjmACOK0YUEYmE4ACMHZwYJc0HAI8bxEou8hkCA6CKsApSgADI9L3KCwrAaKkGBbGA+pR+/BoNBYTiufukCDMTgAcgAApslGYRgAHoYivb9T0xc9OBoTFX3fT8f3/NcgNA9gYFAhwLDgCC8igrgL3DOB4ISD8vz/ADULAjDYLYXDciWOJM04ABeS9rxoO8gmAXJOGiLDhFSZBaIgB54DQSw0AAXQoXiYKGYQCiXVIeLAPi+OEmBMQjccpNSR9nyCCJZLU18TNcCJcgY2JVg2PNWJ4S0TCjUUY2bB0PUzP1VL4oQW1SEIdDgP05AgJQohY11OB89SlggBQI1CpQgm/AAZRhR3HScME4K9mF8KBEG/P1WkiOT3FyCzciPA8QBkrcAyGJUmWYgBadJMxXeqQEakVSl6oMRmI9rkya1Nlzqigtyvct7lMbh+wtYw1LQCBbLgFZpzgXhSEYadG1IxDVEbBcSy6mSygJPprH6L4ZTGOUAQMWMWzpFU1UGYYXG1Qk9SRQ1URNQIQjCSIimEJjEi9DqoZyPClPBzpRCuxBejR+Q6h+JpHvaTM3shaENW+iFfo5fVvBRXkgbwIIsA/HAOAwKI/IdALStSF6HQjbggpCsKOfchNUrCiKoqICBxzbDsuxANJQjkacnAAaxgtaLHFpXG3WfBFCHDKxwnKdGGIvKCpXZGJVRrVGWlLHmmoVonpAFn7nxpBKkJr7Ri1P6DUp410QMWmUxGKJ2eiuS+LgRRYFIVID2sWgABJgDEXblFcA8AG5I9WaPSAeCBNbAePE5TtOLCUTOc9MviiFCcctnYQvi9L5PU5OSvq9zkUIDWNAAFV85bxRUmnZILDQGv1OFfL+4ANQbqAm4LovR5nCfjmn9SRwN7Kx83qfc9Wtvy87jPs8q8U3l6CFbDurGPYd/5AlKt3ECf9UvbcMn/v9+ZgYDVTFEJKAsQQtgjMLJQ199C33trbBojJKROySu/T+n1YR9AAKy+wpjyAOpoaxBjgPWRscUFC5HrqQcGcB4owG9CYOhUtOx4AeDrTgB5yEwAPJwfKUAVgKH9B+Ig44+ziE4HAfIgjYCziUEoSuNC6EwQcFwY2EiWCMDkJIVWyiYC5AAFLiHrgAZR2owLAkNaGCKDMyPIcAvx02IKIqAM4crrBgNOGcH51j52XFZR47C+ECJOrQJSxE0DrDWiQmAvBGBJF4EUTElhjihn8QAKh4Bwo4VjuHRC0XAYi6xJz4F4XoQgUBiIbXsMKYinDGEJSSkZA8fo6nCDoRGMgH5SBNOFGAFxrScluXuD01QWxojiDUvtPOMAXGrWtLtGgOiJk5QAHLQBgBGAAVpUk415mARlyBkhaShQqKzkBwrhPDsISDAA2RGyQ7gzJ0esBZjY5nIAPI4hsBSIxiHbCsNAB4pJBAMlgUMwFgKQFgNsiM7AlDAXbJ2YCWiaBiFakQHUEZaDAXEFgECXz4DLkfMwOQABiAlBS/l9zQGHPpuQPkUuXH8zpQKQVPjBYgCFUKYAwrhQi6WyKbxooxZULFOK8XAUZRGYlZLGXMtIKQCIEZOBsMbCciAZyLn1NybwCZM5GwrGji4opqhqWcDPAIZQuiOHcsQJc3h0BgkHLALkAA+mktJ+x7iVw9a61IqrODqs1VwzgGrNkxLQN+Yig1ynEUkI2SwxSyA0ONjQY4cgMC5DgBgW5+APyQENXrTW1rpzePzjwRMABJcJOscpXmjswacCg/SQGofG3ROUlippLBm3I4Qc32HzX3Yi5hi3y1DcdahazYBbJ2VeEUy5ODGJgG89hHzICLKEEIjshLOCVuAgAeVZaC8FkL1m8p0PypFKLxLosxdi3F+KPzfKJWgElpLxCtQ3TAVqQhWqMtaoIKIA5SC5Hylec1iR2DMC2LiZ1uQzi0F3IIw1CjjqBtOaELVbSFAHkQP4mq2zrI4Y2Y078Os5ChWtOwOQUBvwRBrhCzgiZ07KU4BRqjkTSC0b9HMqlALiODLIxxtaABSHCfpvxcdo/RxjwFmOsdDOxmAlG1rSagLxqJaB/loEE+0zp7AgiWHWJwM4CrDPfl2IQCAYK/S0JjQoxWLiHBYBwJYOjEQGO5CYyxyexEDPUOIXANcjYJkuPKLwFWhY7l8e050/DYAmN8TM10vY1nbMSM/GUxz4hnO4rczM7z8mZ5jOQAuUIeksGoywUVmewouCmN2hYiMpA1iVoCcbAsAROBGfWYgIgzBUYQi1KjQkllEvFfUmMg905w38Ba21jrcAuv0B67agbqprDSFVGN2rJWuC2snmQGschJXPsJcBOgMSAW4neOoVG0g9tTa4GV+ucgpKtReflsgTRtRaie3xMZ5W5CNfMVwXrsBEBHfuKEM7O6CmXdoNd5a7xGhNGsONpLz3OCHeOMd2HMGLCXbe66iuyhtQQlVP4xiOPawOUs5o85VwNXYSEN+GuXChlgCCAeAAIhM3Q1CU5EJgK4AAhJwfnygyBi4PF5ibCm/OpCl4LzguxGecGZ+PNpYAJcq5l5piRcWFXVSPP4xDyGDWSKtehg82S6E8N4Pk1JLqwCEbgIJrgZq2JtGMbskUxisuEHWEZDnNlOkOV9/75ggegzB9D573hGB7eCLYsZxRCUU8wCCNSv0nT5dgeT9qxKYUUoieo9xjzcnFcpP0ipzjNGNM6OpYXrPJfkrkfr2JiTP51Oydq752vynVMV5483gTYBmBF5Ix08z3T08pYs1ZiANngqZYc1apz7Hvvufo/LnzimhKL7jmr9La/7PZc37l7frnFAzJkjozp1ObIi/p+ryjmuWc6/Z634vmxhl84C7JrC61ji6S5AGkCy777yaD5sb67ULv5M5f60K67gHS6QGG5P5u5HirjrhICbhlArqlDIC0J3ANjAonqcrATyKqCbQRgxDMBnrQpwBMEYRNoarAQipirmDThoQz7bIRB1QXSvCwLVAYxki/DPzygtQkbvxYKeyYIfy4LTD4IAI0wxrQBRBt6NJBYhYAD8qQyyfoEYJhNmy0oQo0C6hhYAGAyAUkOYnA4s44PWAA1L0KGrMKFLloIVQIijLLAeEmtAePxoCtaMUjjjAOsN0BspwAALICICB7ihY6ArBBgpLjKTKNgBgFIzJ+gmolLHS5BJBphcCGpPLhDWp0wsCSA5S6G6C9IuLjq5aGy4hYZlGNGVKbRiCTg3ZCCUKhArB9iSJARaLULvKfKsYJBBAQgRDHrspUEwZgDqCwqXrdArDYqLH/ohYsGLEQhnaTwJARgQjSpvpyDjZBDoatCpElhxoQbjrZFGo6IfI3ZyARggYwZoBNIUHsqnrcoXrwp+GCqopoB3qioPoSovEnHvovHvFbCwkgmlSebwbYEHhEa3I2QxD9wORYJh4z5kaYnHCpCiZ0Z+gEk0rV4BGpBkmpDyE6IhF6YNKl7fjUnFRFD9zQE15sbUmcC0mxY6am4Hj+LLqNjPECCvHwlfFsrPi/HnrLh8qAk3rCr3riogSQkyqkownQZwlakIlBTAaDjgaNgWDwlwa4EbhbjW4NilBEDWARi9B2nWDWBCEWw3xYLyEPyII4x4CoLKhWDulfyKG9A+y/x+yqF8iAIhxkBhxBQqS5zRx9I/YcJlwdzpxVyXy1zTKrytxJntxk5pnbx1xLwrwjwlw5lnypndwZm9z9xDxkAlkHzyJbw9xzzHCLzmDLyrRZnrzjyNlHwZm7xZSYANmTwFmqynwpldzpmuAwJsiEjiH3RPzIKvxBRyEKGahag4Ihl4JGhqEGA05Ah5gBSiyOESxQAznajWBSiYzkhekGAHkgjvy9D3wBmajWCuAXQxCwAYgIyEROTCAkRkS94oQgQiS4QWrRT3JKAAWITfgRh8FZD0TokQy2SxgOREQuT7KczDKej3gRymQuzc6lR8zhR4Uzyc5kbsysmInlTmTja1apQ3ikB2arQvixiVy5D3n2BGSlCDTiBICgABCKCSJCB4BLggCuCuBAA"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const unwatch = Actions.amm.watchBurn(config, {
  onBurn(args, log) {
    console.log('args:', args)
  },
})

// Later, stop watching
unwatch()
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

`() => void`

Returns a function to unsubscribe from the event.

## Parameters

### onBurn

* **Type:** `function`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchBurn.md","from":5386,"to":5887}<fsm-4or7z6pudsq>
declare function onBurn(args: Args, log: Log): void

type Args = {
  /** Amount of user token received */
  amountUserToken: bigint
  /** Amount of validator token received */
  amountValidatorToken: bigint
  /** Amount of LP tokens burned */
  liquidity: bigint
  /** Address that removed liquidity */
  sender: Address
  /** Address that received the tokens */
  to: Address
  /** Address of the user token */
  userToken: Address
  /** Address of the validator token */
  validatorToken: Address
}
```

Callback to invoke when liquidity is removed.

### args (optional)

* **Type:** `object`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchBurn.md","from":5988,"to":6244}<fsm-4or7z6pudsq>
type Args = {
  /** Filter by sender address */
  sender?: Address | Address[] | null
  /** Filter by user token address */
  userToken?: Address | Address[] | null
  /** Filter by validator token address */
  validatorToken?: Address | Address[] | null
}
```

Filter events by indexed parameters.

### userToken (optional)

* **Type:** `Address | bigint`

Address or ID of the user token to filter events.

### validatorToken (optional)

* **Type:** `Address | bigint`

Address or ID of the validator token to filter events.

### fromBlock (optional)

* **Type:** `bigint`

Block to start listening from.

### onError (optional)

* **Type:** `function`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchBurn.md","from":6649,"to":6694}<fsm-4or7z6pudsq>
declare function onError(error: Error): void
```

The callback to call when an error occurred when trying to get for a new block.

### poll (optional)

* **Type:** `true`

Enable polling mode.

### pollingInterval (optional)

* **Type:** `number`

Polling frequency (in ms). Defaults to Client's pollingInterval config.

## Viem

* [`amm.watchBurn`](https://viem.sh/tempo/actions/amm.watchBurn)

---

---
url: /tempo/actions/amm.watchMint.md
---
# `amm.watchMint`

Watches for liquidity mint events on the Fee AMM.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchMint.md","from":126,"to":4909}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"3e678dc18ce9b1b0888b0e3f1b0a2e9e066a3d862bdcaf011c8c115c0b244c46","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const unwatch = Actions.amm.watchMint(config, {
  onMint(args, log) {
    console.log('args:', args)
  },
})

// Later, stop watching
unwatch()
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchMint.md","from":4995,"to":5024}<fsm-4or7z6pudsq>
type ReturnType = () => void
```

Returns a function to unsubscribe from the event.

## Parameters

### onMint

* **Type:**

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchMint.md","from":5126,"to":5651}<fsm-4or7z6pudsq>
declare function onMint(args: Args, log: Log): void

type Args = {
  /** Amount of LP tokens minted */
  liquidity: bigint
  /** Address that added liquidity */
  sender: Address
  /** User token details */
  userToken: {
    /** Address of the user token */
    address: Address
    /** Amount of user token added */
    amount: bigint
  }
  /** Validator token details */
  validatorToken: {
    /** Address of the validator token */
    address: Address
    /** Amount of validator token added */
    amount: bigint
  }
}
```

Callback to invoke when liquidity is added.

### sender (optional)

* **Type:** `Address | bigint`

Address or ID of the sender to filter events.

### userToken (optional)

* **Type:** `Address | bigint`

Address or ID of the user token to filter events.

### validatorToken (optional)

* **Type:** `Address | bigint`

Address or ID of the validator token to filter events.

### fromBlock (optional)

* **Type:** `bigint`

Block to start listening from.

### onError (optional)

* **Type:** `(error: Error) => void`

The callback to call when an error occurred when trying to get for a new block.

### poll (optional)

* **Type:** `true`

Enable polling mode for watching events.

### pollingInterval (optional)

* **Type:** `number`

Polling frequency (in ms). Defaults to Client's pollingInterval config.

## Viem

* [`amm.watchMint`](https://viem.sh/tempo/actions/amm.watchMint)

---

---
url: /tempo/actions/amm.watchRebalanceSwap.md
---
# `amm.watchRebalanceSwap`

Watches for rebalance swap events on the Fee AMM.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchRebalanceSwap.md","from":133,"to":5190}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"91e718ca006a23e8682b0ebc2f91d672ae05dd36421745b488980a673c12e660","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const unwatch = Actions.amm.watchRebalanceSwap(config, {
  onRebalanceSwap(args, log) {
    console.log('args:', args)
  },
})

// Later, stop watching
unwatch()
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchRebalanceSwap.md","from":5276,"to":5305}<fsm-4or7z6pudsq>
type ReturnType = () => void
```

Returns a function to unsubscribe from the event.

## Parameters

### onRebalanceSwap

* **Type:** `function`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchRebalanceSwap.md","from":5427,"to":5802}<fsm-4or7z6pudsq>
declare function onRebalanceSwap(args: Args, log: Log): void

type Args = {
  /** Address of the user token */
  userToken: Address
  /** Address of the validator token */
  validatorToken: Address
  /** Address of the swapper */
  swapper: Address
  /** Amount of validator token swapped in */
  amountIn: bigint
  /** Amount of user token received */
  amountOut: bigint
}
```

Callback to invoke when a rebalance swap occurs.

### userToken (optional)

* **Type:** `Address | bigint`

Address or ID of the user token to filter events.

### validatorToken (optional)

* **Type:** `Address | bigint`

Address or ID of the validator token to filter events.

### args (optional)

* **Type:** `object`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchRebalanceSwap.md","from":6134,"to":6392}<fsm-4or7z6pudsq>
type Args = {
  /** Filter by user token address */
  userToken?: Address | Address[] | null
  /** Filter by validator token address */
  validatorToken?: Address | Address[] | null
  /** Filter by swapper address */
  swapper?: Address | Address[] | null
}
```

Filter parameters for the event.

### fromBlock (optional)

* **Type:** `bigint`

Block to start listening from.

### onError (optional)

* **Type:** `function`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/amm.watchRebalanceSwap.md","from":6565,"to":6610}<fsm-4or7z6pudsq>
declare function onError(error: Error): void
```

The callback to call when an error occurred when trying to get for a new block.

### poll (optional)

* **Type:** `true`

Whether to use polling.

### pollingInterval (optional)

* **Type:** `number`

Polling frequency (in ms). Defaults to Client's pollingInterval config.

## Viem

* [`amm.watchRebalanceSwap`](https://viem.sh/tempo/actions/amm.watchRebalanceSwap)

---

---
url: /tempo/connectors/dangerous_secp256k1.md
---
# `dangerous_secp256k1`

Connector for a Secp256k1 EOA.

:::warning
NOT RECOMMENDED FOR PRODUCTION USAGE. This connector stores private keys in clear text, and are bound to the session length of the storage used. Instead, use this connector for testing workflows, like end-to-end tests.
:::

## Usage

```ts [wagmi.config.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/connectors/dangerous_secp256k1.md","from":327,"to":690}<fsm-4or7z6pudsq>
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { dangerous_secp256k1 } from 'wagmi/tempo' // [!code focus]

export const config = createConfig({
  connectors: [dangerous_secp256k1()], // [!code focus]
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempo.id]: http(),
  },
})
```

## Parameters

### account

* **Type:** `LocalAccount`

Optional account to use with connector. If not provided, one is created internally for you.

---

---
url: /tempo/actions/dex.buy.md
---
# `dex.buy`

Buys a specific amount of tokens from the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.buy.md","from":138,"to":6276}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"514f8188da5f3aadb6f821b1369361f48b3a9b8e33f46d5689339bc21bc9aed7","data":"N4Igdg9gJgpgziAXAbVAFwJ4AcZJACwgDcYAnEAGhDRgA808BLAWywlLQAIBBAYzUYQwCKnDQBDDkgCcVADYwwAczT4kAdioTSSmA0Qg+AoSJBzGYXIgAMVXvknj+ZGQF8K6bFYLEXWuvogABTi5uJwAJScAGYArmD8gmCcWJJwMACqYIxocEFEobEwiJxipBZKFJywvCyhcCVgscwARmQRJS2MShZoADrZrOxcqaTpWTmmUBC8CAYAsrFyAljm8JzipWjlypykMFj76WASxskQ0RucTa1knC0YVz0kyXRsliecF/fhMJwAjNZOEFAW8hIo0BEAHQDAYAWk4ABEZg1OPg0GgsA0APTYoiMGDMKFwfDY6azbGxATmATwbGjcbZXKUajiJRzZDIEB0cSsBQslhsDicYApNKZJlwTiuGKkCDMTgAcnxhMVsLADIlkyCioALAAmayKqrSCIDXGcA3Wa0221gEAAXQdom0+l1mjMihUakQgK0kl0gU1E2Z8gsVn+dgcpCcNHIiGk7k8ODwhBI5H89DwITCkU4vBMXALYGi3RKAGEhKWlANBcN81XuiyxJJ9AAOSOe5SqJAANn9Oj0eGL1ZZ5ksSH1UccznjiY81C8qd8GeoAWHhb2MF4MEYWDQJQAKjHhLGkgAlbe7/cs8lzEDH8SnxJCLc7vdoKHN11If7/ACs8hej2iAetogZ4Ps743mGE6ILq04xrOSBtkmi4pgYaZ+GuWYGHWwpGEkpgtlIvoAMxkUB3Y+mBAZDgYhEmGO4ZIAhID2DOcaTr2aGYBhPjpiyNC4SA+FcLAtDfq2v66p2CjUUglGsoOgQScxcFsRxSFcYgZG6rxS6YSuQnrgYcQJGc9yxBgADKGAJAAPJWJbdAAfEEI5lpwznVlUoy8noZCooxwhQhJUItNZdkJFCAAKjjMIFYxOY2SiuR0nCxXKzCMOkDnAAMnBFW+14Hpwj7Pmcl7QWgADcAyuK5AxgAFcCpDuVm2fZvC3iieAAELWVKmxtdujClrwGzMBA8RcN8aAQAA1oocAwmAAwAHIQDQR74LlnD7SN3X4HKkCxMNL7JKo4hcAA7uIkwxOwnCqH82xPnAZ6vgtAxtAdCRyLEsBQF8ySbC0cgzIt9wwNE7B/PsaCxKQ2S7JsRzvOkX7+uySCctytC8qsuBUAABuTuS1kMwqirw+w3TAPndFU6KYtKsrykqAAC91KDl2IFvsaqDEKXCijQQzs9E2Xc7z/OCzAAsOBYcDC2JIo8JdUoytLnOKjzbLy/D2IS2wwsDMWYgNi5SicAAvPm9M0EzShBAVyT5srwglMgpsQIe8BoJYaDOoVL0nm1wyou7xWcL7hJsFCjBQA6JSs1gQQRBQYfuA1ZrrQkm5HEsXAO+I905JrZyreFkVdQkHmpVUMcvUtigAJJgCUirWLQhq8FCg9/saYcLctYAAPJUt3vf94PUKGiPHu8jNJxT2VwaSjqgJGlUvZZ2HzDiLQ3DTbNnclJv2qKoC/7Gpw+/Z2Arj5+TpOOhQXL+cwLKebbCIuy/M6L+CUWTfySlKBE8UYyJTjKtD+XJEbI2ECyQ8+A3oRy+skKCpUgHOhACRfQ/xdSAS7N6DQA4IIGDrtFHqsErCaWjLGFwulUILj4t4LCq5hKBBzIwcIURLZFlShWVKVNRbW1HC6aSvp/xKXkuQxA/ZlJUPYqldSDDELMPjLqHi7DDICWwjw7MhwIA4A4BgKIK9Zrr06N0XoUlSL/F7KQhRIFZAqPoiAaxa8qQaKQKQrS2jJwGX4lwkyIk+ECLFGMLUuR8iFGKFsHYlRqhjSPnIVENw2ikAyl0HoJxxH1ivqGEAd48CLGWHuNYw1kkVC3IceAEIbpJC+JcTY2S7gPCeIwF4nAwQfDmpcFovwARAhBNYAZEJoTqgRMiWYacMRYkQLiFURISRkhRJSakOQCRwHpOKEMpgJC4xQFyHkfISaiWpmLGJjJHo6xlsqAkzBzYakOVvPUi8TT5wtFaW0AL7ROmkU49Qyi3E+j9J4oMHzJj+MQIEphyFyKhM4cZTMvDTHmMwFEI+J8z4nAvvcexJxHH6ENLYMhIE/yUK8Xi0+q80Cd3hcooJyL9SouXIJDF2ZQj8LzCUvIBRAZJLKBUKoNQ6iZMaM0HJeSSX9BFsU2FpTykLBLtUvZVwxW7H2I044pxWnfA6bKrpjxNjPEUP02g7wIRtJ+OkMZwJQQ2vBCcGZBc5kokWZiHEeIXnElJHebZjAaR7IObEo5Qk2QcnOYTS5Aobka0FVLJ5ay3mCp1Fae+ppzTYktBSgFNogX4MIZOf48jgKQspeBLxgqWVaORQBTlRluU4UxXKbFljW7jyJX0EAs9rC8CLSO0dY6i3/H7WSycZEPQQoodCvAY8O72noQutlOkOX6LCei9tJjO1kBxT2xQtjOD9sHcO8dV7r3Wn1FOkF5LpBsXnYgNstLAjLsnn4tdr7G2bpbYY7hplwCtXan8S2EAFADAKKQa2cBINJOcvB/kVA1UPnQZwUmEGFCk04NNKASw/imPxLAWpcBBQKDSZFJQBTbbYbeg4Lg+1yM5TkJIVuL10EDAAFLiAKDZOmH44MIbw9uBw2Q4AKmI8nGAINum3RgC0e4cpbrpDGGtAYaC/j4cI9a0WUo0C3QgKUHAtQJoNiGIMho6oABUPBMNIYQ7h3gbG4BSlujkfAonVDQClHAWI9gNhSiwyYBDUJIauwiKTKoIXhBhbIHKUgmdcNPhBrF5DMAoT3RRslzjN18xPhhpwc6smOO3XKDQDjT5HhbVgFCAAVn57YMBeRrTs9wTgShIYjLkJh+juGVYSASOB1KyNSsLU4OVnIb1jPIFJqYncbniRoGmFSUmDogjpz9ZAWAjWoTsCUJsikbGaBiDhEQfUuooS0GxOILAjB6RykW6tdEzA5AAGIFvwDcytmakINhgCgAMObX2ltiFgKQUg63NtLO29AGAe2DtHf2SdwO53LvXdu/dx7MxvtQlex90HP2Ie5KhOVDDXWIA9b66FnDBXkh/RKyDDzPmqQHRufU16mGdvFH63h6AhGNNgAAPo2ZswAdUkKjJQYvhe7T+JT6n9GvgtHq9uNAiopSwMIFAYa+xri7lerBy2uUaAnDkBgAYcBjqnRmlKcwy1ON/BaCptTPBYrtwM+gx4RxCQQxgFUSAsHJAMZgI8E3YgIQW4GOEG3Qg7ecAd38UIvXtroNg7VzLjXkkteYKtTgNkYCh7jqTSAlXXxE84O3bEE9odbZWdiHniOdDI+xKjs7F2rs3buw9on+O0Bvfe+IOEZeYBwiEHCIncJBBRDhqQAY019cWDn0fM4QuACi8bibFfI7sLnivQg07izhxA6o36NYtrTzLEWdToLkJDSb7A5BQEVBEeqYALRZV6KiO/D+jOkGfyqAm3Bz+0v2P2vwgFdkVF/2MwAFJVYqhFR/9n9X939P8dhcg04YB79jNkCoAgDjMQCqQwCMsoQEt2AghLBbpOB19IcKDFRxdCAzE4Aqh4Ntd6kRkQYHAsAcBLAX8Ig3881MoMCpRyDYNEo3M2Rk9ActgnBoZ3oOpgCVsEtT8P980ipaDEsShGCIBmDWD5Q9A9pdhOC0Q7teDZMhDY58tkAYBhVU5/xZFLDip8sBNyh9woRSB4hO40FcpnIeFgQedEAiBmByJ9RfQ2xfl1DnCuAJ5Vd1cPCvCwAfC4A/CAgAj4cgiQiyJrBpBWFIjY4NguBAjegyAWo5AcdntsQ6BtwqQkhQJ1BfRpAnCiprDbDQgHQ4RyszCyAlFEB9Q701CCj8s2i5BXChNKCMiSiUZQgKjvsqjaAaizhQJewlFrB8irCijJiThSiZij4LAqjhVhcdUlA+iyJdJ1QhFrgAp7YlRxdQ1etzwqcVYhBFR396MsspcghSZEQnxdBYMAASYAFqRKVwAAQiRF+LIFBNJkEMGK/xOFRB+OUDuDuPv04EeK6DizAHBKRL+NBIIK2BJwGDfnVE3yJko3Ok5ww1Jkczpxc3CGswLnPzgBILmjZwdkDBsma15BsgMMIFukzjeM3ASxuM5O5OYF5MSn5MFNZLwwwFpL+AdioOEwUChAVKCD+yqAS1hIX3lKv3C0gNv2wL/yf34LQPzXhMwLRGNNwNNIJNALAGYD1PAINKgJgM4HgPviQNNNQKEMtJ/xtMfwAPwI4wdKdIVLILoKS2VM0PoJ0L0NKAMNUA4PEC4O6L4Nf1hPQO/x9ljNIG0KYKxH0PYOMNTNMJ4MUFk2dA4wSwuM3GBMVNuPuPRKeKxNeN1IjOyzAC+NxLuEBIbLBIhORNIGhKzItJEJKF7Ng1RIeNbPg2xKHLxIJNrLADfmjVOXxnSCuWQHg2Rh3A23r1xB6FUFiBaChALGYEb3h0ayvNgGxAhipzxAxxu3MBaAFn1MawiEdFLR/F0n/GfSrQXVrUCHo3hRpXYiRR0msAA3CR5QMCCG12gCiAjJvwkM+l0AAH4Shqsqh54zEzhQhoFeRURqtkAHQMoiAIBk5gQABqf4L4dMSGVMr81DPqAwf0jjUmIgtAXDFnLzKg8cTLTgSpFYSjAMZoCEKUXgQrP6VINzWTKoPip3AYUsMYLgJnILJ3FIcoI+UgR4NCqQgHEGFPDYKAKAXZIQQ/DS8IUoU8sQHIWooQaDRJPzFgUNdjCbEHDA6IIIMiKLA8pZBvI+MAdQfbFvccWIG7YKyfKQ/ZYKsiR7XoaIKEMifvN7fOIILncSxKBEjYfXEyuS9IEGTy0mWouQKEFfG6ZLAK31BvJvVaJHYNdvNAdHLvLHB7MqtKj7MqyqtAXquEAMSID1Yk8mC/QuYQYRWaG4/8IUl0m/RUAsWaEoWAl/KoRa91c04QnMhsJazgQCDjbikgsLea9ag8e+U6scrahEkoU6kofapQ1bRVEkguQvP4ObTq3q6qmHWq3EeqsKw7JqhmDvZ89qkNcqgnd7Hq9gVffqwa2fZ6RfP4ZfaGlpIQbGVkDcrkXfHcFkIgawKEf4Am60b8h9RSXsKcKlH0JSYCvACLMCzsDdFhNhZMNFNtYxAwS4nBD8I8TBS6aqUqXqWYPACqT6S6EqD8dGstVhOdQC0Cd9SCK8D8emv9FhCiGC3ddm4ILFQ9btd6SqJIAACXCHwBKFJl7kBOONcHflYqFoMCNpJHtWTIM15rOGnV0mkFcVloAnloMD1tFrOHtrUB/XAsZp0X+FcHwQLFgCYCTVFBCm1g5gVCQMNgez9jVljruTiQTt1iTvTSKRpkkW6FTT1ihHfJtjeUuNFC5v3HZjLgri4HjrCjoAiiim6kbhtmbjDh8TQFPUzRvmtHvkfkPmPgZXPi7kzqOW3msDvj3gPg9k/SJR7j7iHRvVXrHX+CXiKk/VPSXv7jXv3oBX1CXhfjrLmsNMVBFqwVMJJEQHvmrs/D9qwUDpYpAFgXECQFAACBWiSCXQQFcFcCAA==="}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const { receipt } = await Actions.dex.buySync(config, {
  amountOut: parseUnits('100', 6),
  maxAmountIn: parseUnits('105', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Transaction hash:', receipt.transactionHash)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.buy` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.buy.md","from":6613,"to":7045}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'

const hash = await Actions.dex.buy(config, {
  amountOut: parseUnits('100', 6),
  maxAmountIn: parseUnits('105', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})
const receipt = await waitForTransactionReceipt(config, { hash })
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.buy.md","from":7072,"to":7153}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Transaction receipt */
  receipt: TransactionReceipt
}
```

## Parameters

### amountOut

* **Type:** `bigint`

Amount of tokenOut to buy.

### maxAmountIn

* **Type:** `bigint`

Maximum amount of tokenIn to spend.

### tokenIn

* **Type:** `Address`

Address of the token to spend.

### tokenOut

* **Type:** `Address`

Address of the token to buy.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`dex.buy`](https://viem.sh/tempo/actions/dex.buy)

---

---
url: /tempo/actions/dex.cancel.md
---
# `dex.cancel`

Cancels an order from the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.cancel.md","from":125,"to":4919}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"8e63dbc2614d60dc2105888794c30ac7532f2a92ed7af97887d3f5dd42573f7c","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const { orderId, receipt } = await Actions.dex.cancelSync(config, {
  orderId: 123n,
})

console.log('Cancelled order ID:', orderId)
// @log: Cancelled order ID: 123n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.cancel` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.cancel.md","from":5259,"to":5628}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { Actions as viem_Actions } from 'viem/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'

const hash = await Actions.dex.cancel(config, {
  orderId: 123n,
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { orderId } }
  = viem_Actions.dex.cancel.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.cancel.md","from":5655,"to":5789}<fsm-4or7z6pudsq>
type ReturnType = {
  /** ID of the cancelled order */
  orderId: bigint
  /** Transaction receipt */
  receipt: TransactionReceipt
}
```

## Parameters

### orderId

* **Type:** `bigint`

ID of the order to cancel.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`dex.cancel`](https://viem.sh/tempo/actions/dex.cancel)

---

---
url: /tempo/actions/dex.createPair.md
---
# `dex.createPair`

Creates a new trading pair on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.createPair.md","from":127,"to":8783}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"898ef8c60c928fbbc1b3ecd918cdf0c00d4ac080a78268a8148b45b02b060db9","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const { key, base, quote, receipt } = await Actions.dex.createPairSync(config, {
  base: '0x20c0000000000000000000000000000000000001',
})

console.log('Pair key:', key)
console.log('Base token:', base)
console.log('Quote token:', quote)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.createPair` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.createPair.md","from":9127,"to":9545}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { Actions as viem_Actions } from 'viem/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'

const hash = await Actions.dex.createPair(config, {
  base: '0x20c0000000000000000000000000000000000001',
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { base, quote } }
  = viem_Actions.dex.createPair.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.createPair.md","from":9572,"to":9801}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Key of the trading pair */
  key: Hex
  /** Address of the base token */
  base: Address
  /** Address of the quote token */
  quote: Address
  /** Transaction receipt */
  receipt: TransactionReceipt
}
```

## Parameters

### base

* **Type:** `Address`

Address of the base token for the pair. The quote token is determined by the base token's quote token.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`dex.createPair`](https://viem.sh/tempo/actions/dex.createPair)

---

---
url: /tempo/actions/dex.getBalance.md
---
# `dex.getBalance`

Gets a user's token balance on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getBalance.md","from":128,"to":5553}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"2cbcd8f2e4514b44f515cfd59cdc515095e16ac4e7309dcfa2a7dbd7df793943","data":"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="}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const balance = await Actions.dex.getBalance(config, {
  account: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  token: '0x20c0000000000000000000000000000000000001',
})

console.log('DEX balance:', balance)
// @log: DEX balance: 1000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getBalance.md","from":5639,"to":5664}<fsm-4or7z6pudsq>
type ReturnType = bigint
```

## Parameters

### account

* **Type:** `Address`

Address of the account.

### token

* **Type:** `Address`

Address of the token.

## Viem

* [`dex.getBalance`](https://viem.sh/tempo/actions/dex.getBalance)

---

---
url: /tempo/actions/dex.getBuyQuote.md
---
# `dex.getBuyQuote`

Gets the quote for buying a specific amount of tokens.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getBuyQuote.md","from":133,"to":5800}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"a420bc920b6563e021956e1161cf4176a0594ca6d74434e3e2fa2b7a9993a741","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const amountIn = await Actions.dex.getBuyQuote(config, {
  amountOut: parseUnits('100', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Amount needed:', amountIn)
// @log: Amount needed: 100300000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getBuyQuote.md","from":5886,"to":5911}<fsm-4or7z6pudsq>
type ReturnType = bigint
```

Returns the amount of `tokenIn` needed to buy the specified `amountOut` of `tokenOut`.

## Parameters

### amountOut

* **Type:** `bigint`

Amount of tokenOut to buy.

### tokenIn

* **Type:** `Address`

Address of the token to spend.

### tokenOut

* **Type:** `Address`

Address of the token to buy.

## Viem

* [`dex.getBuyQuote`](https://viem.sh/tempo/actions/dex.getBuyQuote)

---

---
url: /tempo/actions/dex.getOrder.md
---
# `dex.getOrder`

Gets an order's details from the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getOrder.md","from":134,"to":5091}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"1b4c194e1433ff47798203a8d893230e07a7bba99b163b51514c7b0d01dbdc5f","data":"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="}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const order = await Actions.dex.getOrder(config, {
  orderId: 123n,
})

console.log('Order details:', order)
// @log: Order details: { amount: 100000000n, maker: '0x...', isBid: true, ... }
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getOrder.md","from":5177,"to":5947}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Original order amount */
  amount: bigint
  /** Orderbook key (identifies the trading pair) */
  bookKey: Hex
  /** Tick to flip to when fully filled (for flip orders). For bid flips: must be > tick. For ask flips: must be < tick */
  flipTick: number
  /** Whether this is a bid (true) or ask (false) order */
  isBid: boolean
  /** Whether this is a flip order */
  isFlip: boolean
  /** Address of the user who placed this order */
  maker: Address
  /** Next order ID in the doubly linked list (0 if tail) */
  next: bigint
  /** The order ID */
  orderId: bigint
  /** Previous order ID in the doubly linked list (0 if head) */
  prev: bigint
  /** Remaining amount to be filled */
  remaining: bigint
  /** Price tick */
  tick: number
}
```

Returns the complete order details including the maker's address, order amounts, price tick, linked list pointers, and flip order information.

## Parameters

### orderId

* **Type:** `bigint`

Order ID to query.

## Viem

* [`dex.getOrder`](https://viem.sh/tempo/actions/dex.getOrder)

---

---
url: /tempo/actions/dex.getSellQuote.md
---
# `dex.getSellQuote`

Gets the quote for selling a specific amount of tokens.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getSellQuote.md","from":135,"to":5815}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"e72885ed736301b0d1aa5f428258ba248ff06fde799d2fc7fe974306d5b6b9c7","data":"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="}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const amountOut = await Actions.dex.getSellQuote(config, {
  amountIn: parseUnits('100', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Amount received:', amountOut)
// @log: Amount received: 99700000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getSellQuote.md","from":5901,"to":5926}<fsm-4or7z6pudsq>
type ReturnType = bigint
```

Returns the amount of `tokenOut` received for selling the specified `amountIn` of `tokenIn`.

## Parameters

### amountIn

* **Type:** `bigint`

Amount of tokenIn to sell.

### tokenIn

* **Type:** `Address`

Address of the token to sell.

### tokenOut

* **Type:** `Address`

Address of the token to receive.

## Viem

* [`dex.getSellQuote`](https://viem.sh/tempo/actions/dex.getSellQuote)

---

---
url: /tempo/actions/dex.getTickLevel.md
---
# `dex.getTickLevel`

Gets the tick level information at a specific tick on the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getTickLevel.md","from":163,"to":5884}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"3fba3acc82c4f344f1ecc51d048f896383905db7488d943734d6cdae1b8b032a","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { Tick } from 'viem/tempo'
import { config } from './config'

const level = await Actions.dex.getTickLevel(config, {
  base: '0x20c0000000000000000000000000000000000001',
  tick: Tick.fromPrice('1.001'),
  isBid: true,
})

console.log('Tick level:', level)
// @log: Tick level: { head: 1n, tail: 5n, totalLiquidity: 1000000000n }
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.getTickLevel.md","from":5970,"to":6226}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Order ID of the first order at this tick (0 if empty) */
  head: bigint
  /** Order ID of the last order at this tick (0 if empty) */
  tail: bigint
  /** Total liquidity available at this tick level */
  totalLiquidity: bigint
}
```

Returns the price level information including the order IDs for the head and tail of the FIFO queue at this price level, and the total liquidity available.

## Parameters

### base

* **Type:** `Address`

Address of the base token.

### isBid

* **Type:** `boolean`

Whether to query the bid side (`true`) or ask side (`false`).

### tick

* **Type:** `number`

Price tick to query. Can be created using `Tick.fromPrice()`.

## Viem

* [`dex.getTickLevel`](https://viem.sh/tempo/actions/dex.getTickLevel)

---

---
url: /tempo/actions/dex.place.md
---
# `dex.place`

Places a limit order on the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.place.md","from":126,"to":6672}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"ae78873af261e30e0a9ea1adc6baa89b8d91d755de180f0299788136db141068","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'
import { config } from './config'

const { orderId, receipt } = await Actions.dex.placeSync(config, {
  amount: parseUnits('100', 6),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})

console.log('Order ID:', orderId)
// @log: Order ID: 123n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.place` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.place.md","from":7011,"to":7563}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { Actions as viem_Actions } from 'viem/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'

const hash = await Actions.dex.place(config, {
  amount: parseUnits('100', 6),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { orderId } }
  = viem_Actions.dex.place.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.place.md","from":7590,"to":7985}<fsm-4or7z6pudsq>
type ReturnType = {
  /** ID of the placed order */
  orderId: bigint
  /** Address of the order maker */
  maker: Address
  /** Address of the base token */
  token: Address
  /** Amount of tokens in the order */
  amount: bigint
  /** Whether this is a buy order */
  isBid: boolean
  /** Price tick for the order */
  tick: number
  /** Transaction receipt */
  receipt: TransactionReceipt
}
```

## Parameters

### amount

* **Type:** `bigint`

Amount of tokens to place in the order.

### tick

* **Type:** `number`

Price tick for the order. Use `Tick.fromPrice()` to convert from a price string.

### token

* **Type:** `Address`

Address of the base token.

### type

* **Type:** `OrderType`

Order type - `'buy'` to buy the token, `'sell'` to sell it.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`dex.place`](https://viem.sh/tempo/actions/dex.place)

---

---
url: /tempo/actions/dex.placeFlip.md
---
# `dex.placeFlip`

Places a flip order that automatically flips to the opposite side when filled.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.placeFlip.md","from":155,"to":7335}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"e9b109959543a4af97fa80fd74ff57c367fad28063d8fae2ea79374624391edb","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'
import { config } from './config'

const { orderId, receipt } = await Actions.dex.placeFlipSync(config, {
  amount: parseUnits('100', 6),
  flipTick: Tick.fromPrice('1.01'),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})

console.log('Flip order ID:', orderId)
// @log: Flip order ID: 456n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.placeFlip` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.placeFlip.md","from":7678,"to":8274}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { Actions as viem_Actions } from 'viem/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'

const hash = await Actions.dex.placeFlip(config, {
  amount: parseUnits('100', 6),
  flipTick: Tick.fromPrice('1.01'),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})
const receipt = await waitForTransactionReceipt(config, { hash })

const { args: { orderId } }
  = viem_Actions.dex.placeFlip.extractEvent(receipt.logs)
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.placeFlip.md","from":8301,"to":8773}<fsm-4or7z6pudsq>
type ReturnType = {
  /** ID of the placed flip order */
  orderId: bigint
  /** Address of the order maker */
  maker: Address
  /** Address of the base token */
  token: Address
  /** Amount of tokens in the order */
  amount: bigint
  /** Whether this is a buy order */
  isBid: boolean
  /** Price tick for the order */
  tick: number
  /** Target tick to flip to when order is filled */
  flipTick: number
  /** Transaction receipt */
  receipt: TransactionReceipt
}
```

## Parameters

### amount

* **Type:** `bigint`

Amount of tokens to place in the order.

### flipTick

* **Type:** `number`

Target tick to flip to when order is filled. Must be greater than `tick` for buy orders, less than `tick` for sell orders.

### tick

* **Type:** `number`

Price tick for the order. Use `Tick.fromPrice()` to convert from a price string.

### token

* **Type:** `Address`

Address of the base token.

### type

* **Type:** `'buy' | 'sell'`

Order type - `'buy'` to buy the token, `'sell'` to sell it.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`dex.placeFlip`](https://viem.sh/tempo/actions/dex.placeFlip)

---

---
url: /tempo/actions/dex.sell.md
---
# `dex.sell`

Sells a specific amount of tokens on the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.sell.md","from":138,"to":6272}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"997af5c0532953dd4e2e196ac8b932f9108ab9fe48dbcca2fc81f6d18ce19b1e","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { config } from './config'

const { receipt } = await Actions.dex.sellSync(config, {
  amountIn: parseUnits('100', 6),
  minAmountOut: parseUnits('95', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Transaction hash:', receipt.transactionHash)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.sell` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.sell.md","from":6610,"to":7042}<fsm-4or7z6pudsq>
import { Actions } from 'wagmi/tempo'
import { waitForTransactionReceipt } from 'wagmi/actions'
import { parseUnits } from 'viem'

const hash = await Actions.dex.sell(config, {
  amountIn: parseUnits('100', 6),
  minAmountOut: parseUnits('95', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})
const receipt = await waitForTransactionReceipt(config, { hash })
```

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.sell.md","from":7069,"to":7150}<fsm-4or7z6pudsq>
type ReturnType = {
  /** Transaction receipt */
  receipt: TransactionReceipt
}
```

## Parameters

### amountIn

* **Type:** `bigint`

Amount of tokenIn to sell.

### minAmountOut

* **Type:** `bigint`

Minimum amount of tokenOut to receive.

### tokenIn

* **Type:** `Address`

Address of the token to sell.

### tokenOut

* **Type:** `Address`

Address of the token to receive.

### account (optional)

* **Type:** `Account | Address`

Account that will be used to send the transaction. Defaults to connected Wagmi account.

### feeToken (optional)

* **Type:** `Address | bigint`

Fee token for the transaction.

Can be a TIP-20 token address or ID.

### feePayer (optional)

* **Type:** `Account | true`

Fee payer for the transaction.

Can be a [Viem Account](https://viem.sh/docs/accounts/local/privateKeyToAccount), or `true` if a [Fee Payer Service](https://docs.tempo.xyz/sdk/typescript/server/handler.feePayer) will be used.

### gas (optional)

* **Type:** `bigint`

Gas limit for the transaction.

### maxFeePerGas (optional)

* **Type:** `bigint`

Max fee per gas for the transaction.

### maxPriorityFeePerGas (optional)

* **Type:** `bigint`

Max priority fee per gas for the transaction.

### nonce (optional)

* **Type:** `number`

Nonce for the transaction.

### nonceKey (optional)

* **Type:** `'expiring' | bigint`

Nonce key for the transaction.

### validBefore (optional)

* **Type:** `number`

Unix timestamp before which the transaction must be included.

### validAfter (optional)

* **Type:** `number`

Unix timestamp after which the transaction can be included.

### throwOnReceiptRevert (optional)

* **Type:** `boolean`
* **Default:** `true`

Whether to throw an error if the transaction receipt indicates a revert. Only applicable to `*Sync` actions.

## Viem

* [`dex.sell`](https://viem.sh/tempo/actions/dex.sell)

---

---
url: /tempo/hooks/dex.useBalance.md
---
# `dex.useBalance`

Gets a user's token balance on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useBalance.md","from":125,"to":5462}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"86f30c8b6ecfcd05a596ac74359c0fbce656e58c96f45bc8cceeb1ce8f608b07","data":"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"}
import { Hooks } from 'wagmi/tempo'

const { data: balance } = Hooks.dex.useBalance({
  account: '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEbb',
  token: '0x20c0000000000000000000000000000000000001',
})

console.log('DEX balance:', balance)
// @log: DEX balance: 1000000000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `dex.getBalance` Return Type](/tempo/actions/dex.getBalance#return-type)

## Parameters

See [Wagmi Action `dex.getBalance` Parameters](/tempo/actions/dex.getBalance#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`dex.getBalance`](/tempo/actions/dex.getBalance)

---

---
url: /tempo/hooks/dex.useBuy.md
---
# `dex.useBuy`

Buys a specific amount of tokens from the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useBuy.md","from":138,"to":7274}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"19b864958a3edb268ed55df991f577eacfa8b004aba94539562aed8b4486c2ef","data":"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="}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const buySync = Hooks.dex.useBuySync()

// Call `mutate` in response to user action (e.g. button click, form submission)
buySync.mutate({
  amountOut: parseUnits('100', 6),
  maxAmountIn: parseUnits('105', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Transaction hash:', buySync.data?.receipt.transactionHash)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.buy` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useBuy.md","from":7609,"to":8124}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { useWaitForTransactionReceipt } from 'wagmi'

const buy = Hooks.dex.useBuy()
const { data: receipt } = useWaitForTransactionReceipt({ hash: buy.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
buy.mutate({
  amountOut: parseUnits('100', 6),
  maxAmountIn: parseUnits('105', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.buy` Return Type](/tempo/actions/dex.buy#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.buy` Parameters](/tempo/actions/dex.buy#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.buy`](/tempo/actions/dex.buy)

---

---
url: /tempo/hooks/dex.useBuyQuote.md
---
# `dex.useBuyQuote`

Gets the quote for buying a specific amount of tokens.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useBuyQuote.md","from":130,"to":5743}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"cb4e5f5fb447a1a65ef7af20e203bda1f35f12b1e876616083f30b47831f53fb","data":"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"}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const { data: quote } = Hooks.dex.useBuyQuote({
  amountOut: parseUnits('100', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Amount needed:', quote)
// @log: Amount needed: 100300000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `dex.getBuyQuote` Return Type](/tempo/actions/dex.getBuyQuote#return-type)

## Parameters

See [Wagmi Action `dex.getBuyQuote` Parameters](/tempo/actions/dex.getBuyQuote#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`dex.getBuyQuote`](/tempo/actions/dex.getBuyQuote)

---

---
url: /tempo/hooks/dex.useCancel.md
---
# `dex.useCancel`

Cancels an order from the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useCancel.md","from":125,"to":5873}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"d99005d358f82f6b8da0b324b8d268d476741fc0146d122b7f8fb1d35c61bdc0","data":"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="}
import { Hooks } from 'wagmi/tempo'

const cancelSync = Hooks.dex.useCancelSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
cancelSync.mutate({
  orderId: 123n,
})

console.log('Cancelled order ID:', cancelSync.data?.orderId)
// @log: Cancelled order ID: 123n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.cancel` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useCancel.md","from":6211,"to":6670}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { useWaitForTransactionReceipt } from 'wagmi'

const cancel = Hooks.dex.useCancel()
const { data: receipt } = useWaitForTransactionReceipt({ hash: cancel.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
cancel.mutate({
  orderId: 123n,
})

if (receipt) {
  const { args: { orderId } }
    = Actions.dex.cancel.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.cancel` Return Type](/tempo/actions/dex.cancel#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.cancel` Parameters](/tempo/actions/dex.cancel#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.cancel`](/tempo/actions/dex.cancel)

---

---
url: /tempo/hooks/dex.useCreatePair.md
---
# `dex.useCreatePair`

Creates a new trading pair on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useCreatePair.md","from":127,"to":8287}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"30ad47475bf43802763bb99c5cf8fdf2fdf294d49b87a8e6428158f4753de2e3","data":"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"}
import { Hooks } from 'wagmi/tempo'

const createPairSync = Hooks.dex.useCreatePairSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
createPairSync.mutate({
  base: '0x20c0000000000000000000000000000000000001',
})

console.log('Base token:', createPairSync.data?.base)
console.log('Quote token:', createPairSync.data?.quote)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.createPair` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useCreatePair.md","from":8629,"to":9149}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { useWaitForTransactionReceipt } from 'wagmi'

const createPair = Hooks.dex.useCreatePair()
const { data: receipt } = useWaitForTransactionReceipt({ hash: createPair.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
createPair.mutate({
  base: '0x20c0000000000000000000000000000000000001',
})

if (receipt) {
  const { args: { base, quote } }
    = Actions.dex.createPair.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.createPair` Return Type](/tempo/actions/dex.createPair#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.createPair` Parameters](/tempo/actions/dex.createPair#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.createPair`](/tempo/actions/dex.createPair)

---

---
url: /tempo/hooks/dex.useOrder.md
---
# `dex.useOrder`

Gets an order's details from the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useOrder.md","from":131,"to":5440}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"1815c3299836587ecb4ba2019dc58a529df6920eadae785fd12d0d622fd85358","data":"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="}
import { Hooks } from 'wagmi/tempo'

const { data: order } = Hooks.dex.useOrder({
  orderId: 123n,
})

console.log('Order details:', order)
// @log: Order details: { amount: 100000000n, maker: '0x...', isBid: true, ... }
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `dex.getOrder` Return Type](/tempo/actions/dex.getOrder#return-type)

## Parameters

See [Wagmi Action `dex.getOrder` Parameters](/tempo/actions/dex.getOrder#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`dex.getOrder`](/tempo/actions/dex.getOrder)

---

---
url: /tempo/hooks/dex.usePlace.md
---
# `dex.usePlace`

Places a limit order on the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.usePlace.md","from":126,"to":7655}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"dc89ef7c90b6e3e69c1c36d86e7178af7ac3a72d19bcb225b4b1bdc2a7afa924","data":"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"}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'

const placeSync = Hooks.dex.usePlaceSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
placeSync.mutate({
  amount: parseUnits('100', 6),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})

console.log('Order ID:', placeSync.data?.orderId)
// @log: Order ID: 123n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.place` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.usePlace.md","from":7992,"to":8631}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'
import { useWaitForTransactionReceipt } from 'wagmi'

const place = Hooks.dex.usePlace()
const { data: receipt } = useWaitForTransactionReceipt({ hash: place.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
place.mutate({
  amount: parseUnits('100', 6),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})

if (receipt) {
  const { args: { orderId } }
    = Actions.dex.place.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.place` Return Type](/tempo/actions/dex.place#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.place` Parameters](/tempo/actions/dex.place#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.place`](/tempo/actions/dex.place)

---

---
url: /tempo/hooks/dex.usePlaceFlip.md
---
# `dex.usePlaceFlip`

Places a flip order that automatically flips to the opposite side when filled.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.usePlaceFlip.md","from":155,"to":8394}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"0b032ce2f26b3ba60b7d704cf92957c90fd7feb051b6dc255273d25ecb860c75","data":"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="}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'

const placeFlipSync = Hooks.dex.usePlaceFlipSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
placeFlipSync.mutate({
  amount: parseUnits('100', 6),
  flipTick: Tick.fromPrice('1.01'),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})

console.log('Flip order ID:', placeFlipSync.data?.orderId)
// @log: Flip order ID: 456n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.placeFlip` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.usePlaceFlip.md","from":8735,"to":9430}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { Actions } from 'viem/tempo'
import { parseUnits } from 'viem'
import { Tick } from 'viem/tempo'
import { useWaitForTransactionReceipt } from 'wagmi'

const placeFlip = Hooks.dex.usePlaceFlip()
const { data: receipt } = useWaitForTransactionReceipt({ hash: placeFlip.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
placeFlip.mutate({
  amount: parseUnits('100', 6),
  flipTick: Tick.fromPrice('1.01'),
  tick: Tick.fromPrice('0.99'),
  token: '0x20c0000000000000000000000000000000000001',
  type: 'buy',
})

if (receipt) {
  const { args: { orderId } }
    = Actions.dex.placeFlip.extractEvent(receipt.logs)
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.placeFlip` Return Type](/tempo/actions/dex.placeFlip#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.placeFlip` Parameters](/tempo/actions/dex.placeFlip#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.placeFlip`](/tempo/actions/dex.placeFlip)

---

---
url: /tempo/hooks/dex.useSell.md
---
# `dex.useSell`

Sells a specific amount of tokens on the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useSell.md","from":138,"to":7269}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"ae5fe3560e82c82e12f7f413d98649d47715c71ac035ce263b44bcd061feddc4","data":"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"}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const sellSync = Hooks.dex.useSellSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
sellSync.mutate({
  amountIn: parseUnits('100', 6),
  minAmountOut: parseUnits('95', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Transaction hash:', sellSync.data?.receipt.transactionHash)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.sell` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useSell.md","from":7605,"to":8123}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { useWaitForTransactionReceipt } from 'wagmi'

const sell = Hooks.dex.useSell()
const { data: receipt } = useWaitForTransactionReceipt({ hash: sell.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
sell.mutate({
  amountIn: parseUnits('100', 6),
  minAmountOut: parseUnits('95', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.sell` Return Type](/tempo/actions/dex.sell#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.sell` Parameters](/tempo/actions/dex.sell#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.sell`](/tempo/actions/dex.sell)

---

---
url: /tempo/hooks/dex.useSellQuote.md
---
# `dex.useSellQuote`

Gets the quote for selling a specific amount of tokens.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useSellQuote.md","from":132,"to":5744}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"e032bbb5ac251a0290eacf6fd15a7b454e27c2398bf4e185fb4d8d10e5253e5b","data":"N4Igdg9gJgpgziAXAbVAFwJ4AcZJACwgDcYAnEAGhDRgA808BLAWywlLQAIAJCCAawRU4aAIYckATioAbGGADmafEgCsVMaQUwGiELwFCQMxmFyIADFQDG+caOs1yiSQF8K6bOYLEylanS6IAAUoiaicACUnABmAK5gjowQYJxY4nAwAKpgjGhwwURhcTCInCKkpgoUnLDWLGFwZWBxzABGZJFlbYwKpmgAOrms7FzppJk5eUZQENYIegCycTJojFgm8Jyi5WiVipykMFhHmWBiaymcEDHbnC3tZJxtGHd9JKl0bGbn17dtERgnAAjBZOMFQV8UvI0JEAHRDIYAWk4ABE5k1OPg0GgsE0APT4oiMGDMOFwfD42bzfFxNYmNbwfHjSa5fL+MQKBbIZAgOiiVhyfwsNgcTjANIZbJsuCcVyxUgQZicADkxNJKsRYBZ0umwRVABYAEwWFU1SSRIaEzjGix2+0OsAgAC6zuEml0BvUxnkShUiFBGnE2iCOqm7NkpnMwJsdlIDicUncnhweEIJHIGkCeGCJwgOA4GGiUFEYm6vX6nAAPpwErAYlGoP5qQsQAAVfBAmQRLhwOLWazwODxGQyV6nCAyEhQWqlnYxdicZRAgCOJVIGARYC1Ha7PfK/cHcGHKzHh3gk+ns7EsUXy84a7Im61Q13nG7IgPA6HI7PE6nMAziWN4LqQS6dg+67PtuMFvh+vaHj+p7jheAFAXOt5gfej4bluO4QfBX5Hieo4oXAl6Ade853hBOGbv4IjiLoADs0g+ooyhIAaQZaDoeDAaI/gmGYSAAMyxvYjh+IgAAcybUF4aa+JmAT0Hg1gpJ+a4QDQ5Z9L8NZ1jADZmE2VAtngcH7n237Hr+ZEUehIE0auUFwgxHpIDJ3pyBx/repoIZ4NpNBCVGYkSfGUnOMCBryZgqZ6OmfhZmpegiqMPB8IIHlMVIPm+pxiABcGfF6AYOWRiJiDiSAtiSYmiBGnFHgKYlPgZhy2bpSMYqwLQuUSAGFgxuxfoRdQpVBP1YXVbV9VRY1okWPFilJcpXVpSA8SJJcqRxJkADKMCjgAinEOkwAAPAAwikDbVM8FbnAAfLm9jMDoZCYhVcBwv1cIHTAx1nRdNBwgACh9X0TLd929DUPT6WgL1dFlhj/XQgNHSdMjnZdcIAEo6HEpBgAAasU11I/0L1DGAArwOkg61jjoOXc2GJ4BVmGcCGawHNhYNAqB5S41UdxwDg9QNtY2zMBACRcDcS4CPIf0cqIXJIDyfK0AKGy4FQAAGpv5LQQwZWKEq/XKCpKqqADuWvMIw+I0CMmowTtSRXAAglgWDBNEwBDJwnAaWAn4SgJNSMHAAAyECiFAEvygAvOjgiY7Q2PA7j+M0MEoepOH8uK+cACSYBlGGMr6qCpo1AAbJEFBh2XaBq2A1dlCqFi0Ca1hwiPwLAmaHfh13/DyAA8nSfcD0PI9wiaE+l64loweHjC3ME8dJynVTREcaCk6kV2p0QL2H6nigr1dVKMNfHen+fnCX8/L0AKK0NLNAznnriBe4oBKuEflfOmYBXBDFNsbF0FBeTjAFP4ZBn0nCyhRFDeM6DvruTdLyN+ZMjDnSfOePsqxOCOzyPgcCQIBQV2Vrcaec86TnkHM/QC+C3QgEYkNUEBU/JIGBEaHiQU9BAxBnjYWs1zDzTjAmaSokWopm8MlFSNAtq5kVAWTA0QGFK17k9ZGnN5h4D9grJWfxVYzx7qkLuYtRzuXdHlAMRpRFjSKjJMRZUQAGKrk6Kq5huJ1QUdFJARpVrtXUZtIIoRwhRElBMXU+RChUzKBUKoNQ6gNBkJiB4HRSBoxpucS2vUxhSnDDMLmSwVhrA2CSWUOxMkHCOCceAMJSzJFSCrHYBSngvDeJwz4f9oS/BVgCTIIIwQQgsFCH4sI8JgBROieYZRsS4gJESEkZIKRUgxLSekeRGnMkqTKTW2sUC8n5IKI2IArZcAlHXaYdsYiKmVGqHZXshjPNSYaNe5ot7WltA6UFTpXQuP4aJDxvlxrDR8aGM50xZFcUioomKkTWoJTURtVKcS8y6KLDY+QRjjYDwACTABaQoVw8DzI1JAH7KAUBTiyhVveFh9iICOJkM43hnkAyqGbrIQq/pmIIrwJy6uKLipovCU1KJOLOp4pzASsgejiVgCAWUMltBKXUtpaY1sTKWVDmsRy7uqt2EwE4XyvhugjTAlqrCrxEq9CcqATK4VoSGrSUxaopSyrVJBAZp9KWDggSR3InIIYRQwJRsnKUTgd0o6JqNZZCCxsE1yGNpwBWUAVhAjzMSWATTygijkLUGAbQ4gKH0goCOmlE3gVLJweO5bXbdiwty5cQwABSogiiHWsJULAXBs1Ak+vVXIcBlTFsYLAGcgzHbVueIqR2mQJhLLfPmwtnAoQcFlGgR23KpYwBlowOWGkRgLKaFqAAVJwP2nBjYpujTAXN1gPyymocoPNOhCBQFlDZWhEQX0TrhDICAChg7GxqFmptcg4RkEVKQWD2wwAzgQ6mpDzsyboeUK26wohUgdFZpRBxjtKg0CtSR14AA5aAMA4QACtgN7BgAKLcj7n0KCgwCGQ4HEMfrbVHMQiRI3wwUKTCj3KqN5CBA45Axs8zEXJGgWYdJjbOmCBsvEiBCSQFgGxuE7AFD7JpN2GgIgkREGanCWg+JRBYDdqpoccJsTMBkAAYjc8eEQmnYQYagEMZTfm/oBZQ9p3TOJ9OGaYyZszFm4D4is/ANAtn7OOec65xUanPM+fC5F0gRS4ScDfHxiAAmhM4ZE8R0jQIgYzl/YQNhDyJb3mNkZ0oE7c27qQ1qAA+ve+9AB1cQuRFAjcG2UCr/GwiNtq9cNoLHz1oBVLKdBgGmlHHuDa5c8bNLxxoOcMcQw4AYESPgRUkADrvkYDPOha6IAbqeH7CGlcj2djIqSNocgaiQDAuIRT33FtwGOzCM7DMLtXZu4rWUJhHthEEzpTsYFGOwFY+xo4Ao/qcGOiDoEynIA0auOFzgld8Sz2i3prZ3XEtaGS6l0s6XMsGgc05lzzI8vuYK950QSIScwCRCkJE4WkTJGiKBIYCtdumFAswLpKQlm/wNpWg6HWIKVeq9h99xtEBajgWxoYEGoMwZVJ2Uccn2AyCgCqSIABuK0+JOAQ32PkdZuNrekFtzUBxAXFaDESMJyD0H9SW6g5wAApHAM0Tsbd28d87137vMQR+977q1Ae6Qm5Dyh9gwQzCO04N/ErBeVSjcIPmOANRyJbYlgCGcdhA7yEAvbpPYBrRu/6LKfPYEw1wC1vQzDuwHD8CXFFRTp6NMoYN53l34dS+obKJXvgeJa9KgAw3lOWJnM4FMsnsu2wuDIBgEUGQzpiqCsP2XVtw7R1oDhKQBI1cOzxxTZorghemOICIMwAM0KAYMkQKC+t+XAs8K2a2T+L+YAb+cAH+gQ4I3Wv+/+y0kgNUwBN+4crayB/QZADMMg3OcwQ4+IdA56dI3SiAzEzEAYkgWBx+nAp+5+zoSIVGe+ZAiAzcTURo9BraZ+YQ9+6wX+uB5w+BYQRBxEpBtA5Be0VBXBzcFgIBR+DBIhTgBB+IiupgpB5+g21KTUokNUWoUaXAoaQImcFejAo4nAhMVWpg5EYAKoTuwetWcIeGYAwQxsqIJG2gYElKphrgAAhGiN4WQAEcbB3l3qnmUF4YoE8KNpYYJjYT0KmmAEETET4QEX7tPrACVrAqbFqKrrcqzJrkCK+sJp+t+nPnkcbMbs4Z+IHpwJnCGIdBxgKIdJvoQI7MHE4cYfuiVo0XzDoC0TjswO0Z9J0d0bnmJnmhgG+s2pnEXmDomnCHMXIMEIHjUChh3jLrMSHmbuHl7lQgnvbk4ZET3p7lbkcT7lAFkdcDnmAMwLsS4fsRbocTHnHiqCetcSccnt3ucGnocV8Zng4oHjsascxn3oXjAMXkvuXqvtXhvvXgcI3rvi3qZO3qcS7n8R7owbCaQCvlXuvuUJvsoNvk3uwaZG6FaihkYZpCYYzAMRYVYUkXYSkI4WCSHm4R4ekU8H4YzIEcEbEaQGEREViVEYKT4ZwPEcybYSkWkSEcKbcTSWAHAhctyLyJkHcsgORKTIODprTgZviH0MoHEG0HCNeviPTilt1viH9lVkSFlqlowG0PiBBmxpEC6DwvahEsxM6qKkgOKpNLxEEBOjKmxAtOikgCtFimtB1ClMGjmFttANEOCaHjBgPkPgAPxlB0Y1Arz5h7RhDYK445lgAYDIDOhoxEAQALrggADUwI1wGYUGKcHp9KZieg2JR63Kxs2eaAuaLWe2jswkzGnAywqw6wlawYrQMIso9WzwRaEQmQNxVCNCdCQwDYEwXATW2wX2RalQiuG4/6x4Q+wW2wVhKcqchZgmO5YGfYbQIgeQFBKQsaVMwGLAlh4gVqYW7uMQwQokkQNOsWhpiuYAzEpmjOwkcQjmoFYuQ+KWoFok3O/QMQcIokHmaAXmW8wQ9405n0/x2wu2yOkox4smjBxsFBvKCupYsG+psWdOCWf0SWLYzO1mGWdm7O2WXOlFGFXm3mlF1FaAglSIwYUQ8IhupstRvRGkVimcqgPRexYeKoMl5wZQUeduNQKlsImJKe5xjaSsZQ6gWeGmoJdRyxLxWliAceWlopul/xZQllnARl/uJl9xcCWoBO5FPFgltFMWmyhpVpEF5mLFaWNmHFHOOWhylhvFPmAl7AiuQl8VpYIlWgiSossuQI8uSVe0fKnI6pvCpgg4/gRAFgcIwIZVdonpkKDqMko0Lq/otUgUviZuYZcqjUckMZ0SuKCZegvRIUSaJSXAhkmGxkjY6aegVkn4NkxE9k5CjkVEvMQsT4dqAqy0gicKJUwZwUMiQSUgbVSi/qbU3gnI/gpheALV1VYkIiIqQilgKqegFijC1qnCUAZQkgkgzEYKMqY8+1zgK0PCGksATA5S4oWcso8obyDsnxLsbsHsbAXsDyoNvy4N9sHy6ozA3ydRjyVEZQ/Vdsmcv0OcecUihcMAxcHc/iaARiyNDcdocerc7cpcUqNcqoS8Fg1goKnNXN3NPNI068U83c2qrNg87NvNYt4t9oRo68m8tJzxSlj1ViRwHC04VlNQ/VW8/g6CgkiAoAgQ6s3SkqCArgrgQAA==="}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const { data: quote } = Hooks.dex.useSellQuote({
  amountIn: parseUnits('100', 6),
  tokenIn: '0x20c0000000000000000000000000000000000001',
  tokenOut: '0x20c0000000000000000000000000000000000002',
})

console.log('Amount received:', quote)
// @log: Amount received: 99700000n
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `dex.getSellQuote` Return Type](/tempo/actions/dex.getSellQuote#return-type)

## Parameters

See [Wagmi Action `dex.getSellQuote` Parameters](/tempo/actions/dex.getSellQuote#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`dex.getSellQuote`](/tempo/actions/dex.getSellQuote)

---

---
url: /tempo/hooks/dex.useTickLevel.md
---
# `dex.useTickLevel`

Gets the tick level information at a specific tick on the Stablecoin DEX orderbook.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useTickLevel.md","from":160,"to":5909}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"57b65b077fbeb672f0d0226a0c174adf10d17a4561575135f580ae6d087d726d","data":"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="}
import { Hooks } from 'wagmi/tempo'
import { Tick } from 'viem/tempo'

const { data: level } = Hooks.dex.useTickLevel({
  base: '0x20c0000000000000000000000000000000000001',
  tick: Tick.fromPrice('1.001'),
  isBid: true,
})

console.log('Tick level:', level)
// @log: Tick level: { head: 1n, tail: 5n, totalLiquidity: 1000000000n }
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Return Type

See [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook return types.

### data

See [Wagmi Action `dex.getTickLevel` Return Type](/tempo/actions/dex.getTickLevel#return-type)

## Parameters

See [Wagmi Action `dex.getTickLevel` Parameters](/tempo/actions/dex.getTickLevel#parameters)

### query

See the [TanStack Query query docs](https://tanstack.com/query/v5/docs/framework/react/reference/useQuery) for more info hook parameters.

## Action

* [`dex.getTickLevel`](/tempo/actions/dex.getTickLevel)

---

---
url: /tempo/hooks/dex.useWatchFlipOrderPlaced.md
---
# `dex.useWatchFlipOrderPlaced`

Watches for flip order placed events on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useWatchFlipOrderPlaced.md","from":147,"to":4937}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"ec2db8af3c2ec972afbe7d0d286151f1c33da31056ce694679eda2d35e5d89ec","data":"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="}
import { Hooks } from 'wagmi/tempo'

Hooks.dex.useWatchFlipOrderPlaced({
  onFlipOrderPlaced: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `dex.watchFlipOrderPlaced` Parameters](/tempo/actions/dex.watchFlipOrderPlaced#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`dex.placeFlip`](/tempo/actions/dex.placeFlip)
* [`dex.watchFlipOrderPlaced`](/tempo/actions/dex.watchFlipOrderPlaced)

---

---
url: /tempo/hooks/dex.useWatchOrderCancelled.md
---
# `dex.useWatchOrderCancelled`

Watches for order cancelled events on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useWatchOrderCancelled.md","from":144,"to":4616}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"ee48b5f79e7f2895e840942af571c220f1e3dff682b0163666b36294801e6325","data":"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="}
import { Hooks } from 'wagmi/tempo'

Hooks.dex.useWatchOrderCancelled({
  onOrderCancelled: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `dex.watchOrderCancelled` Parameters](/tempo/actions/dex.watchOrderCancelled#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`dex.cancel`](/tempo/actions/dex.cancel)
* [`dex.watchOrderCancelled`](/tempo/actions/dex.watchOrderCancelled)

---

---
url: /tempo/hooks/dex.useWatchOrderFilled.md
---
# `dex.useWatchOrderFilled`

Watches for order filled events on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useWatchOrderFilled.md","from":138,"to":4756}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"d6ebca7ccec7392508f050d98ee570f2e62a86cf7af165696dace79303079a4f","data":"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"}
import { Hooks } from 'wagmi/tempo'

Hooks.dex.useWatchOrderFilled({
  onOrderFilled: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `dex.watchOrderFilled` Parameters](/tempo/actions/dex.watchOrderFilled#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`dex.buy`](/tempo/actions/dex.buy)
* [`dex.watchOrderFilled`](/tempo/actions/dex.watchOrderFilled)

---

---
url: /tempo/hooks/dex.useWatchOrderPlaced.md
---
# `dex.useWatchOrderPlaced`

Watches for order placed events on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useWatchOrderPlaced.md","from":138,"to":4844}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"3e7dca1cf113bef29341a671f24d7e6ec1d9eec74f78c78ceefe4f494ee9551f","data":"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="}
import { Hooks } from 'wagmi/tempo'

Hooks.dex.useWatchOrderPlaced({
  onOrderPlaced: (args, log) => {
    console.log('args:', args)
  },
})
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

## Parameters

See [Wagmi Action `dex.watchOrderPlaced` Parameters](/tempo/actions/dex.watchOrderPlaced#parameters)

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

## Action

* [`dex.place`](/tempo/actions/dex.place)
* [`dex.watchOrderPlaced`](/tempo/actions/dex.watchOrderPlaced)

---

---
url: /tempo/hooks/dex.useWithdraw.md
---
# `dex.useWithdraw`

Withdraws tokens from the Stablecoin DEX to your wallet.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useWithdraw.md","from":132,"to":6780}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"1ba49397fce40202581f9380b2e1c849c02f8b39dbc63f623cec1edd321703c9","data":"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="}
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'

const withdrawSync = Hooks.dex.useWithdrawSync()

// Call `mutate` in response to user action (e.g. button click, form submission)
withdrawSync.mutate({
  amount: parseUnits('100', 6),
  token: '0x20c0000000000000000000000000000000000001',
})

console.log('Transaction hash:', withdrawSync.data?.receipt.transactionHash)
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

### Asynchronous Usage

The example above uses a `*Sync` variant of the action, that will wait for the transaction to be included before returning.

If you are optimizing for performance, you should use the non-sync `dex.withdraw` action and wait for inclusion manually:

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/hooks/dex.useWithdraw.md","from":7120,"to":7555}<fsm-4or7z6pudsq>
import { Hooks } from 'wagmi/tempo'
import { parseUnits } from 'viem'
import { useWaitForTransactionReceipt } from 'wagmi'

const withdraw = Hooks.dex.useWithdraw()
const { data: receipt } = useWaitForTransactionReceipt({ hash: withdraw.data })

// Call `mutate` in response to user action (e.g. button click, form submission)
withdraw.mutate({
  amount: parseUnits('100', 6),
  token: '0x20c0000000000000000000000000000000000001',
})
```

## Return Type

See [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook return types.

### data

See [Wagmi Action `dex.withdraw` Return Type](/tempo/actions/dex.withdraw#return-type)

### mutate/mutateAsync

See [Wagmi Action `dex.withdraw` Parameters](/tempo/actions/dex.withdraw#parameters)

## Parameters

### config

`Config | undefined`

[`Config`](https://wagmi.sh/react/api/createConfig#config) to use instead of retrieving from the nearest [`WagmiProvider`](https://wagmi.sh/react/api/WagmiProvider).

### mutation

See the [TanStack Query mutation docs](https://tanstack.com/query/v5/docs/framework/react/reference/useMutation) for more info hook parameters.

## Action

* [`dex.withdraw`](/tempo/actions/dex.withdraw)

---

---
url: /tempo/actions/dex.watchFlipOrderPlaced.md
---
# `dex.watchFlipOrderPlaced`

Watches for flip order placed events on the Stablecoin DEX.

## Usage

::: code-group

```ts twoslash [example.ts]
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.watchFlipOrderPlaced.md","from":147,"to":5292}<fsm-4or7z6pudsq>
// @twoslash-cache: {"v":1,"hash":"546bd06c6d922c9812fee931dd4652721a211f4c197b95a0862ff50f70b8b057","data":"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"}
// @filename: config.ts
// @errors: 2322
import type { Config } from 'wagmi'
export const config = {} as Config
// @filename: example.ts
// ---cut---
import { Actions } from 'wagmi/tempo'
import { config } from './config'

const unwatch = Actions.dex.watchFlipOrderPlaced(config, {
  onFlipOrderPlaced(args, log) {
    console.log('args:', args)
  },
})

// Later, stop watching
unwatch()
```

```ts \[config.ts]
import { createConfig, http } from 'wagmi'
import { tempoTestnet } from 'wagmi/chains'
import { KeyManager, webAuthn } from 'wagmi/tempo'

export const config = createConfig({
  connectors: [
    webAuthn({
      keyManager: KeyManager.localStorage(),
    }),
  ],
  chains: [tempoTestnet],
  multiInjectedProviderDiscovery: false,
  transports: {
    [tempoTestnet.id]: http(),
  },
})

```

:::

## Return Type

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.watchFlipOrderPlaced.md","from":5378,"to":5407}<fsm-4or7z6pudsq>
type ReturnType = () => void
```

Returns a function to unsubscribe from the event.

## Parameters

### onFlipOrderPlaced

* **Type:** `function`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.watchFlipOrderPlaced.md","from":5531,"to":5991}<fsm-4or7z6pudsq>
declare function onFlipOrderPlaced(args: Args, log: Log): void

type Args = {
  /** ID of the placed order */
  orderId: bigint
  /** Address that placed the order */
  maker: Address
  /** Address of the base token */
  token: Address
  /** Amount of tokens in the order */
  amount: bigint
  /** Whether this is a buy order */
  isBid: boolean
  /** Price tick for the order */
  tick: number
  /** Target tick to flip to when filled */
  flipTick: number
}
```

Callback to invoke when a flip order is placed.

### args (optional)

* **Type:** `object`

```ts
// <fsm-4or7z6pudsq>{"path":"/vercel/path0/site/tempo/actions/dex.watchFlipOrderPlaced.md","from":6094,"to":6315}<fsm-4or7z6pudsq>
type Args = {
  /** Filter by order ID */
  orderId?: bigint | bigint[] | null
  /** Filter by maker address */
  maker?: Address | Address[] | null
  /** Filter by token address */
  token?: Address | Address[] | null
}
```

Filter parameters for the event subscription.

### maker (optional)

* **Type:** `Address`

Address of the maker to filter events.
