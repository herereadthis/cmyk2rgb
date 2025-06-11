# cmyk2rgb

Python Package to convert CMYK colors to RGB using ICC profiles

```shell
# Setup
poetry install
```
## Usage

```shell
cmyk2rgb convert [OPTIONS] <C> <M> <Y> <K>
```

### Arguments

* `<C>` `<M>` `<Y>` `<K>` — CMYK values as integers, from 0 to 100.

### Options

* `--profile [fogra|japan|swop]` - ICC profile aliases.
  * If you omit `--profile`, the prompt will ask you to choose one

### Examples

```shell
poetry run cmyk2rgb convert 84 15 32 0 --profile japan
poetry run cmyk2rgb convert 84 15 32 0
```

### ICC Profiles

Currently, there is support for 3 profiles, which should cover most of your needs

| Code    | Region             | Profile Name                    | Source                                                                 |
|---------|--------------------|----------------------------------|------------------------------------------------------------------------|
| `fogra` | Europe             | Coated_Fogra39L_VIGC_300.icc    | [color.org](https://www.color.org/registry/Coated_Fogra39L_VIGC_300.xalter) |
| `japan` | Japan              | JapanColor2011Coated.icc        | [color.org](https://www.color.org/registry/JapanColor2011Coated.xalter)     |
| `swop`  | North America (US) | SWOP2006_Coated3v2.icc          | [color.org](https://www.color.org/registry/SWOP2006_Coated3v2.xalter)       |

