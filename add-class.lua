-- eg. Input
-- <li><p>old</p></li>
-- Output:
-- <li>old</li>
function removePTagsInLiBlocks (element)
  if element.tag == "BulletList" or element.tag == "OrderedList" then
    -- Iterate through the list items
    for i, item in ipairs(element.content) do
      -- Check if the item contains a paragraph block
      if item.tag == "Plain" then
        -- Remove the paragraph block and keep its inline contents
        element.content[i] = pandoc.Span(item.content)
      end
    end
  end
  return element
end

return {
  { Inline = removePTagsInLiBlocks },
  { Block = removePTagsInLiBlocks }
}
