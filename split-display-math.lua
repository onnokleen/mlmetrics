local function is_display_math_inline(inline)
  return inline.t == "Math" and inline.mathtype == "DisplayMath"
end

local function is_display_math_wrapper(inline)
  if inline.t ~= "Span" then
    return false
  end

  if #inline.content ~= 1 then
    return false
  end

  return is_display_math_inline(inline.content[1])
end

local function is_split_point(inline)
  return is_display_math_inline(inline) or is_display_math_wrapper(inline)
end

local function is_equation_label(inline)
  return inline.t == "Str" and inline.text:match("^%{#eq[%w%-:_]*%}$") ~= nil
end

function Para(para)
  local has_display_math = false

  for _, inline in ipairs(para.content) do
    if is_split_point(inline) then
      has_display_math = true
      break
    end
  end

  if not has_display_math then
    return nil
  end

  local blocks = {}
  local buffer = {}

  local function flush_buffer()
    if #buffer > 0 then
      blocks[#blocks + 1] = pandoc.Para(buffer)
      buffer = {}
    end
  end

  local index = 1
  while index <= #para.content do
    local inline = para.content[index]

    if is_split_point(inline) then
      flush_buffer()

      local equation_inlines = { inline }
      local next_inline = para.content[index + 1]
      local after_next_inline = para.content[index + 2]

      if next_inline and (next_inline.t == "Space" or next_inline.t == "SoftBreak") and after_next_inline and is_equation_label(after_next_inline) then
        equation_inlines[#equation_inlines + 1] = next_inline
        equation_inlines[#equation_inlines + 1] = after_next_inline
        index = index + 2
      elseif next_inline and is_equation_label(next_inline) then
        equation_inlines[#equation_inlines + 1] = next_inline
        index = index + 1
      end

      blocks[#blocks + 1] = pandoc.Div(
        { pandoc.Para(equation_inlines) },
        pandoc.Attr("", { "display-math-block" })
      )
    else
      buffer[#buffer + 1] = inline
    end

    index = index + 1
  end

  flush_buffer()
  return blocks
end